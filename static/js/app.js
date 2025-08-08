const { useState, useEffect } = React;

// Navigation Component
const Navigation = ({ activePage, setActivePage }) => {
    return (
        <nav className="navbar">
            <div className="nav-container">
                <a href="#" className="logo" onClick={() => setActivePage('home')}>
                    <img src="/static/images/logo.png" alt="JIYER" className="logo-img" />
                    JIYER
                </a>
                <ul className="nav-links">
                    <li><a 
                        href="#" 
                        className={activePage === 'home' ? 'active' : ''} 
                        onClick={() => setActivePage('home')}
                    >
                        Company Introduction
                    </a></li>
                    <li><a 
                        href="#" 
                        className={activePage === 'products' ? 'active' : ''} 
                        onClick={() => setActivePage('products')}
                    >
                        Products
                    </a></li>
                    <li><a 
                        href="#" 
                        className={activePage === 'contact' ? 'active' : ''} 
                        onClick={() => setActivePage('contact')}
                    >
                        Contact Us
                    </a></li>
                </ul>
            </div>
        </nav>
    );
};

// Home/Company Introduction Component
const HomePage = () => {
    const [companyInfo, setCompanyInfo] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/api/company-info')
            .then(response => response.json())
            .then(data => {
                setCompanyInfo(data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching company info:', error);
                setLoading(false);
            });
    }, []);

    if (loading) {
        return (
            <div className="loading">
                <div className="spinner"></div>
            </div>
        );
    }

    return (
        <div className="main-content">
            <div className="hero">
                <div className="container">
                    <h1>Welcome to {companyInfo.name}</h1>
                    <p>{companyInfo.description}</p>
                </div>
            </div>

            <div className="container">
                <div className="grid">
                    <div className="card">
                        <h2>🌍 Our Mission</h2>
                        <p>{companyInfo.mission}</p>
                    </div>
                    <div className="card">
                        <h2>🎯 Our Vision</h2>
                        <p>{companyInfo.vision}</p>
                    </div>
                    <div className="card">
                        <h2>📈 Company Stats</h2>
                        <div>
                            <h3>Founded</h3>
                            <p>{companyInfo.founded}</p>
                            <h3>Employees</h3>
                            <p>{companyInfo.employees}+</p>
                            <h3>Headquarters</h3>
                            <p>{companyInfo.headquarters}</p>
                        </div>
                    </div>
                </div>

                <div className="card">
                    <h2>🌱 Why Choose JIYER?</h2>
                    <div className="grid">
                        <div>
                            <h3>Innovation</h3>
                            <p>Cutting-edge environmental technology solutions that push the boundaries of what's possible.</p>
                        </div>
                        <div>
                            <h3>Sustainability</h3>
                            <p>Every product and service is designed with environmental impact in mind.</p>
                        </div>
                        <div>
                            <h3>Quality</h3>
                            <p>Rigorous testing and quality control ensure reliable, long-lasting solutions.</p>
                        </div>
                        <div>
                            <h3>Support</h3>
                            <p>Dedicated customer support team to help you implement and maintain our solutions.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

// Products Component
const ProductsPage = () => {
    return (
        <div className="main-content">
            <div className="hero">
                <div className="container">
                    <h1>Our Products</h1>
                    <p>Coming soon...</p>
                </div>
            </div>
        </div>
    );
};

// Contact Component
const ContactPage = () => {
    const [contactInfo, setContactInfo] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/api/contact')
            .then(response => response.json())
            .then(data => {
                setContactInfo(data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching contact info:', error);
                setLoading(false);
            });
    }, []);



    if (loading) {
        return (
            <div className="loading">
                <div className="spinner"></div>
            </div>
        );
    }

    return (
        <div className="main-content">
            <div className="hero">
                <div className="container">
                    <h1>Contact Us</h1>
                    <p>Get in touch with our team for any inquiries or support</p>
                </div>
            </div>

            <div className="container">
                <div className="grid">
                    <div className="card">
                        <h2>📍 Contact Information</h2>
                        <div>
                            <h3>Address</h3>
                            <p>{contactInfo.address}</p>
                            <h3>Phone</h3>
                            <p>{contactInfo.phone}</p>
                            <h3>Email</h3>
                            <p>{contactInfo.email}</p>
                            <h3>Working Hours</h3>
                            <p>{contactInfo.working_hours}</p>
                        </div>
                    </div>

                    <div className="card">
                        <h2>🌐 Social Media</h2>
                        <div>
                            <p><a href={contactInfo.social_media.linkedin} target="_blank" rel="noopener noreferrer">LinkedIn</a></p>
                            <p><a href={contactInfo.social_media.twitter} target="_blank" rel="noopener noreferrer">Twitter</a></p>
                            <p><a href={contactInfo.social_media.facebook} target="_blank" rel="noopener noreferrer">Facebook</a></p>
                        </div>
                    </div>
                </div>


            </div>
        </div>
    );
};

// Footer Component
const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-content">
                <div className="footer-section">
                    <h3>
                        <img src="/static/images/logo.png" alt="JIYER" className="footer-logo" />
                        JIYER
                    </h3>
                    <p>Leading environmental technology solutions for a sustainable future.</p>
                </div>
                <div className="footer-section">
                    <h3>Quick Links</h3>
                    <a href="#home">Company Introduction</a>
                    <a href="#products">Products</a>
                    <a href="#contact">Contact Us</a>
                </div>
                <div className="footer-section">
                    <h3>Contact Info</h3>
                    <p>123 Green Street, Shenzhen, China</p>
                    <p>+86 123 4567 8900</p>
                    <p>info@jiyer.com</p>
                </div>
                <div className="footer-section">
                    <h3>Follow Us</h3>
                    <a href="#" target="_blank">LinkedIn</a>
                    <a href="#" target="_blank">Twitter</a>
                    <a href="#" target="_blank">Facebook</a>
                </div>
            </div>
            <div className="footer-bottom">
                <p>&copy; 2025 JIYER. All rights reserved. | Building a greener future together.</p>
            </div>
        </footer>
    );
};

// Main App Component
const App = () => {
    const [activePage, setActivePage] = useState('home');

    const renderPage = () => {
        switch (activePage) {
            case 'home':
                return <HomePage />;
            case 'products':
                return <ProductsPage />;
            case 'contact':
                return <ContactPage />;
            default:
                return <HomePage />;
        }
    };

    return (
        <div>
            <Navigation activePage={activePage} setActivePage={setActivePage} />
            {renderPage()}
            <Footer />
        </div>
    );
};

// Render the app
ReactDOM.render(<App />, document.getElementById('root'));
