# JIYER Environmental Technology Website

A modern, responsive website for JIYER Environmental Technology Company built with Flask (backend) and React (frontend).

## Features

- **Company Introduction**: Detailed information about JIYER's mission, vision, and company statistics
- **Contact Us**: Contact information
- **Responsive Design**: Mobile-friendly interface
- **Environmental Theme**: Green color palette reflecting the company's eco-friendly focus

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: React (JavaScript)
- **Database**: SQLite
- **Styling**: CSS3 with custom environmental theme
- **Icons**: Emoji icons for visual appeal

## Installation and Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd jiyer_website
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   ./start.sh
   ```
   
   Or manually:
   ```bash
   python app.py
   ```

4. **Access the website**
   Open your browser and navigate to `http://localhost:8080`

## Project Structure

```
jiyer_website/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── start.sh              # Startup script
├── jiyer.db              # SQLite database (auto-generated)
├── templates/
│   ├── index.html        # Main HTML template
│   ├── login.html        # Admin login page
│   └── manage.html       # Admin management panel
├── static/
│   ├── css/
│   │   └── styles.css    # Custom CSS styles
│   ├── js/
│   │   └── app.js        # React frontend application
│   └── images/           # Image assets (if any)
└── README.md             # Project documentation
```

## API Endpoints

- `GET /` - Main page (served at http://localhost:8080)
- `GET /api/company-info` - Company information
- `GET /api/contact` - Contact information

## Admin Panel

- `GET /login` - Admin login page
- `GET /manage` - Admin management panel (requires login)
- `POST /update_company` - Update company information
- `POST /update_contact` - Update contact information

**Admin Password**: `jiyer_admin`

## Design Features

- **Environmental Theme**: Light green color palette
- **Modern UI**: Clean, professional design
- **Responsive**: Works on all device sizes
- **Interactive**: Smooth animations and hover effects
- **Accessible**: Proper semantic HTML and ARIA labels

## Development

The project uses:
- Flask for the backend API
- React for the frontend (loaded via CDN)
- Custom CSS for styling
- Babel for JSX compilation

## License

© 2024 JIYER Environmental Technology. All rights reserved.