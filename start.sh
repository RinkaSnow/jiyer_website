#!/bin/bash

# JIYER Website Startup Script
# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🌱 Starting JIYER Website...${NC}"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 is not installed. Please install Python3 first.${NC}"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is not installed. Please install pip3 first.${NC}"
    exit 1
fi

# Check if virtual environment exists, if not create one
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
pip install -r requirements.txt

# Check if Flask is installed
if ! python -c "import flask" &> /dev/null; then
    echo -e "${RED}❌ Flask installation failed. Please check your internet connection and try again.${NC}"
    exit 1
fi

# Check if curl is installed for health check
if ! command -v curl &> /dev/null; then
    echo -e "${YELLOW}⚠️  curl not found. Health check will be skipped.${NC}"
    SKIP_HEALTH_CHECK=true
else
    SKIP_HEALTH_CHECK=false
fi

echo -e "${GREEN}✅ All dependencies are installed!${NC}"
echo "=================================================="
echo -e "${BLUE}🚀 Starting Flask server...${NC}"
echo -e "${GREEN}📱 Backend API will be available at: http://localhost:8080${NC}"
echo -e "${GREEN}🌐 Frontend will be available at: http://localhost:3000${NC}"
echo -e "${YELLOW}🛑 Press Ctrl+C to stop all servers${NC}"
echo "=================================================="

# Function to cleanup background processes
cleanup() {
    echo -e "\n${YELLOW}🛑 Stopping all servers...${NC}"
    kill $FLASK_PID $REACT_PID 2>/dev/null
    exit 0
}

# Set trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Start Flask backend in background
echo -e "${BLUE}🚀 Starting Flask backend server...${NC}"
python app.py &
FLASK_PID=$!

# Wait a moment for Flask to start
sleep 3

# Check if Flask started successfully
if [ "$SKIP_HEALTH_CHECK" = false ]; then
    if ! curl -s http://localhost:8080 > /dev/null; then
        echo -e "${RED}❌ Flask backend failed to start${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Flask backend health check passed${NC}"
else
    echo -e "${YELLOW}⚠️  Skipping health check (curl not available)${NC}"
fi

echo -e "${GREEN}✅ Flask backend is running on port 8080${NC}"

# Start React development server (if you want to use a separate React dev server)
# For now, we'll just serve the static files through Flask
echo -e "${BLUE}🌐 Frontend is served through Flask at http://localhost:8080${NC}"

# Keep the script running
echo -e "${GREEN}🎉 All servers are running!${NC}"
echo -e "${GREEN}📱 Open your browser and go to: http://localhost:8080${NC}"

# Wait for user to stop
wait
