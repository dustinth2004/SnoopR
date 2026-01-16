#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Global variables
VENV_DIR="snoopr_env"
REQUIREMENTS_FILE="requirements.txt"
START_SCRIPT="start_snoopr.sh"

# Trap Ctrl+C
trap 'echo -e "\n${RED}Setup cancelled by user.${NC}"; exit 1' INT

# Helper Functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

print_banner() {
    echo -e "${CYAN}"
    echo "   _____                            ____  "
    echo "  / ___/____  ____  ____  ____     / __ \ "
    echo "  \__ \/ __ \/ __ \/ __ \/ __ \   / /_/ / "
    echo " ___/ / / / / /_/ / /_/ / /_/ /  / _, _/  "
    echo "/____/_/ /_/\____/\____/ .___/  /_/ |_|   "
    echo "                      /_/                 "
    echo -e "${NC}"
    echo -e "${YELLOW}Welcome to the Ultimate SnoopR Setup Assistant!${NC}"
    echo "This script will hold your hand from start to finish."
    echo "---------------------------------------------------"
}

ask_user() {
    # $1 = prompt message
    # returns 0 for yes, 1 for no
    while true; do
        read -p "$(echo -e "${YELLOW}$1 [y/N]: ${NC}")" yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* ) return 1;;
            "" ) return 1;; # Default to No
            * ) echo "Please answer yes or no.";;
        esac
    done
}

ask_user_default_yes() {
    # $1 = prompt message
    # returns 0 for yes, 1 for no
    while true; do
        read -p "$(echo -e "${YELLOW}$1 [Y/n]: ${NC}")" yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* ) return 1;;
            "" ) return 0;; # Default to Yes
            * ) echo "Please answer yes or no.";;
        esac
    done
}

check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_warn "This script works best if run as sudo to install system packages."
        if ask_user "Do you want to restart this script with sudo?"; then
            sudo "$0" "$@"
            exit $?
        else
            log_warn "Continuing without sudo. Some steps might fail."
        fi
    fi
}

update_system() {
    if ask_user_default_yes "Do you want to update your system package list (apt update)?"; then
        log_info "Updating package lists..."
        apt-get update
        if [ $? -eq 0 ]; then
            log_success "System updated."
        else
            log_error "Failed to update system."
        fi
    else
        log_info "Skipping system update."
    fi
}

install_dependencies() {
    log_info "Checking system dependencies..."

    DEPS="python3 python3-pip python3-venv git kismet rtl-sdr rtl-433 librtlsdr-dev"

    if ask_user_default_yes "Do you want to install/verify the following packages: $DEPS?"; then
        log_info "Installing dependencies..."
        apt-get install -y $DEPS
        if [ $? -eq 0 ]; then
            log_success "Dependencies installed."
        else
            log_error "Failed to install some dependencies. Please check your internet connection or package manager."
        fi
    fi
}

setup_python_env() {
    log_info "Setting up Python environment..."

    if [ ! -d "$VENV_DIR" ]; then
        if ask_user_default_yes "Create a virtual environment in ./$VENV_DIR?"; then
            python3 -m venv "$VENV_DIR"
            if [ $? -eq 0 ]; then
                log_success "Virtual environment created."
            else
                log_error "Failed to create virtual environment."
                return
            fi
        fi
    else
        log_info "Virtual environment already exists."
    fi

    # Install requirements
    if [ -f "$REQUIREMENTS_FILE" ]; then
        if ask_user_default_yes "Install Python dependencies from $REQUIREMENTS_FILE?"; then
            source "$VENV_DIR/bin/activate"
            pip install --upgrade pip
            pip install -r "$REQUIREMENTS_FILE"
            # Optional: Install pylint as mentioned in memory
            pip install pylint
            if [ $? -eq 0 ]; then
                log_success "Python dependencies installed."
            else
                log_error "Failed to install Python dependencies."
            fi
            deactivate
        fi
    else
        log_error "$REQUIREMENTS_FILE not found!"
    fi
}

check_hardware() {
    log_info "Checking hardware..."

    if lsusb | grep -i "RTL"; then
        log_success "RTL-SDR device(s) detected via USB."
    else
        log_warn "No RTL-SDR devices found via lsusb. Make sure your dongle is plugged in."
    fi

    if command -v rtl_test &> /dev/null; then
        log_info "Running a quick rtl_test (Ctrl+C if it hangs)..."
        timeout 5s rtl_test -t
        if [ $? -eq 0 ]; then
            log_success "RTL-SDR is communicating correctly."
        else
            log_warn "rtl_test failed or timed out. You might need to configure udev rules or blacklist dvb_usb_rtl28xxu."
        fi
    fi
}

configure_permissions() {
    log_info "Checking permissions..."

    # Get the real user if running as sudo
    REAL_USER=${SUDO_USER:-$USER}

    if groups "$REAL_USER" | grep -q "kismet"; then
        log_success "User '$REAL_USER' is already in the 'kismet' group."
    else
        if ask_user "Add user '$REAL_USER' to the 'kismet' group (recommended for capturing)?"; then
            usermod -aG kismet "$REAL_USER"
            log_success "Added '$REAL_USER' to 'kismet' group. You may need to logout and login again."
        fi
    fi

    if groups "$REAL_USER" | grep -q "plugdev"; then
        log_success "User '$REAL_USER' is already in the 'plugdev' group."
    else
        if ask_user "Add user '$REAL_USER' to the 'plugdev' group (for RTL-SDR access)?"; then
            usermod -aG plugdev "$REAL_USER"
            log_success "Added '$REAL_USER' to 'plugdev' group. You may need to logout and login again."
        fi
    fi
}

create_startup_script() {
    log_info "Creating helper script: $START_SCRIPT"

    cat > "$START_SCRIPT" <<EOF
#!/bin/bash
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "\${GREEN}Starting SnoopR... \${NC}"

# Activate Venv
source "$(pwd)/$VENV_DIR/bin/activate"

# Check if Kismet is running
if ! pgrep -x "kismet" > /dev/null; then
    echo -e "\${RED}Kismet is not running.\${NC}"
    read -p "Do you want to start Kismet now? (y/N) " yn
    if [[ \$yn =~ ^[Yy]$ ]]; then
        echo "Starting Kismet in the background..."
        sudo kismet --daemonize
        sleep 5
    else
        echo "Warning: SnoopR needs a Kismet DB file to work. Make sure one exists."
    fi
fi

# Function to find latest kismet file
find_latest_kismet() {
    ls -t *.kismet 2>/dev/null | head -n 1
}

LATEST_KISMET=\$(find_latest_kismet)

if [ -z "\$LATEST_KISMET" ]; then
    echo -e "\${RED}No .kismet files found in current directory!\${NC}"
    echo "Please run Kismet for a while to generate a database."
    exit 1
fi

echo -e "\${GREEN}Using database: \$LATEST_KISMET\${NC}"

# Start HTTP Server in background
if ! pgrep -f "http.server" > /dev/null; then
    echo "Starting map server on port 8000..."
    python3 -m http.server 8000 &
    HTTP_PID=\$!
    echo "Map available at: http://localhost:8000/SnoopR_Map.html"
else
    echo "Map server already running."
fi

# Run SnoopR
echo "Running SnoopR (Press Ctrl+C to stop)..."
python3 SnoopR.py --db-path "\$LATEST_KISMET" --output-map SnoopR_Map.html

# Cleanup
if [ ! -z "\$HTTP_PID" ]; then
    kill \$HTTP_PID
fi
EOF

    chmod +x "$START_SCRIPT"
    log_success "Created $START_SCRIPT"
}

run_diagnostics() {
    echo ""
    echo -e "${YELLOW}=== Final System Diagnostics ===${NC}"

    echo -n "Python: "
    if command -v python3 &> /dev/null; then echo -e "${GREEN}OK ($(python3 --version))${NC}"; else echo -e "${RED}MISSING${NC}"; fi

    echo -n "Pip: "
    if command -v pip3 &> /dev/null; then echo -e "${GREEN}OK${NC}"; else echo -e "${RED}MISSING${NC}"; fi

    echo -n "Kismet: "
    if command -v kismet &> /dev/null; then echo -e "${GREEN}OK${NC}"; else echo -e "${RED}MISSING${NC}"; fi

    echo -n "RTL-SDR Tools: "
    if command -v rtl_test &> /dev/null; then echo -e "${GREEN}OK${NC}"; else echo -e "${RED}MISSING${NC}"; fi

    echo -n "RTL-433: "
    if command -v rtl_433 &> /dev/null; then echo -e "${GREEN}OK${NC}"; else echo -e "${RED}MISSING${NC}"; fi

    echo -n "SnoopR Dependencies: "
    if [ -d "$VENV_DIR" ]; then
        source "$VENV_DIR/bin/activate"
        if python3 -c "import folium, pandas, cbor2, jinja2, jsonschema" 2>/dev/null; then
            echo -e "${GREEN}OK${NC}"
        else
            echo -e "${RED}MISSING (Check requirements)${NC}"
        fi
        deactivate
    else
         echo -e "${RED}VENV MISSING${NC}"
    fi

    echo ""
    log_success "Setup Complete!"
    echo -e "You can now run: ${GREEN}./$START_SCRIPT${NC} to start everything."
}

# Main Execution
print_banner
check_root
update_system
install_dependencies
setup_python_env
check_hardware
configure_permissions
create_startup_script
run_diagnostics
