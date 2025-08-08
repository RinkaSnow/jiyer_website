const { useState, useEffect } = React;

// Navigation Component
const Navigation = ({ activePage, navigateTo }) => {
    return (
        <nav className="navbar">
            <div className="nav-container">
                <a href="#" className="logo" onClick={(e) => { e.preventDefault(); navigateTo('home'); }}>
                    <img src="/static/images/logo.png" alt="JIYER" className="logo-img" />
                    JIYER
                </a>
                <ul className="nav-links">
                    <li><a 
                        href="#" 
                        className={activePage === 'home' ? 'active' : ''} 
                        onClick={(e) => { e.preventDefault(); navigateTo('home'); }}
                    >
                        Company Introduction
                    </a></li>
                    <li><a 
                        href="#" 
                        className={activePage === 'products' ? 'active' : ''} 
                        onClick={(e) => { e.preventDefault(); navigateTo('products'); }}
                    >
                        Products
                    </a></li>
                    <li><a 
                        href="#" 
                        className={activePage === 'contact' ? 'active' : ''} 
                        onClick={(e) => { e.preventDefault(); navigateTo('contact'); }}
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
const ProductsPage = ({ navigateTo }) => {
    const [products, setProducts] = useState([]);
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('all');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        Promise.all([
            fetch('/api/products').then(res => res.json()),
            fetch('/api/categories').then(res => res.json())
        ]).then(([productsData, categoriesData]) => {
            setProducts(productsData.products || []);
            setCategories(categoriesData.categories || []);
            setLoading(false);
        }).catch(error => {
            console.error('Error fetching data:', error);
            setLoading(false);
        });
    }, []);

    const filteredProducts = selectedCategory === 'all' 
        ? products 
        : products.filter(product => product.category === selectedCategory);

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
                    <h1>Our Products</h1>
                    <p>Discover our innovative environmental technology solutions</p>
                </div>
            </div>

            <div className="container">
                {/* Category Filter */}
                <div className="category-filter">
                    <button 
                        className={`filter-btn ${selectedCategory === 'all' ? 'active' : ''}`}
                        onClick={() => setSelectedCategory('all')}
                    >
                        All Categories
                    </button>
                    {categories.map(category => (
                        <button 
                            key={category}
                            className={`filter-btn ${selectedCategory === category ? 'active' : ''}`}
                            onClick={() => setSelectedCategory(category)}
                        >
                            {category}
                        </button>
                    ))}
                </div>

                {/* Products Grid */}
                <div className="products-grid">
                    {filteredProducts.map(product => (
                        <div key={product.id} className="product-card">
                            <div className="product-image">
                                {product.images && product.images.length > 0 ? (
                                    <img src={product.images[0]} alt={product.name} />
                                ) : (
                                    <div className="placeholder-image">
                                        📦
                                    </div>
                                )}
                            </div>
                            <div className="product-content">
                                <h3>{product.name}</h3>
                                <p className="product-code">Code: {product.code}</p>
                                <p className="product-category">{product.category}</p>
                                <p className="product-description">{product.description}</p>
                                <button 
                                    className="btn"
                                    onClick={() => navigateTo('product-detail', product.id)}
                                >
                                    View Details
                                </button>
                            </div>
                        </div>
                    ))}
                </div>

                {filteredProducts.length === 0 && (
                    <div className="no-products">
                        <p>No products found in this category.</p>
                    </div>
                )}
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

// Product Detail Component
const ProductDetailPage = ({ productId, navigateTo }) => {
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(`/api/products/${productId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Product not found');
                    window.location.href = '/';
                    return;
                }
                setProduct(data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching product:', error);
                window.location.href = '/';
            });
    }, [productId]);

    if (loading) {
        return (
            <div className="loading">
                <div className="spinner"></div>
            </div>
        );
    }

    if (!product) {
        return <div>Product not found</div>;
    }

    return (
        <div className="main-content">
            <div className="hero">
                <div className="container">
                    <h1>{product.name}</h1>
                    <p>{product.category} • Code: {product.code}</p>
                </div>
            </div>

            <div className="container">
                <div className="product-detail">
                    {/* Product Images */}
                    {product.images && product.images.length > 0 && (
                        <div className="product-images">
                            <div className="main-image">
                                <img src={product.images[0]} alt={product.name} />
                            </div>
                            {product.images.length > 1 && (
                                <div className="image-gallery">
                                    {product.images.slice(1).map((image, index) => (
                                        <img key={index} src={image} alt={`${product.name} ${index + 2}`} />
                                    ))}
                                </div>
                            )}
                        </div>
                    )}

                    {/* Product Information */}
                    <div className="product-info">
                        <h2>Product Details</h2>
                        <div className="product-meta">
                            <p><strong>Category:</strong> {product.category}</p>
                            <p><strong>Product Code:</strong> {product.code}</p>
                        </div>
                        <div className="product-description">
                            <h3>Description</h3>
                            <p>{product.description}</p>
                        </div>
                        <button 
                            className="btn"
                            onClick={() => navigateTo('products')}
                        >
                            ← Back to Products
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

// Main App Component
const App = () => {
    const [activePage, setActivePage] = useState('home');
    const [productId, setProductId] = useState(null);

    // Handle navigation and URL changes
    useEffect(() => {
        const handleNavigation = () => {
            const path = window.location.pathname;
            
            // Check for product detail page
            const productMatch = path.match(/^\/product\/(\d+)$/);
            if (productMatch) {
                setProductId(productMatch[1]);
                setActivePage('product-detail');
                return;
            }
            
            // Check for other pages
            if (path === '/') {
                setActivePage('home');
                setProductId(null);
            } else if (path === '/products') {
                setActivePage('products');
                setProductId(null);
            } else if (path === '/contact') {
                setActivePage('contact');
                setProductId(null);
            }
        };

        // Initial navigation
        handleNavigation();

        // Listen for browser back/forward
        window.addEventListener('popstate', handleNavigation);

        return () => {
            window.removeEventListener('popstate', handleNavigation);
        };
    }, []);

    // Navigation function
    const navigateTo = (page, productId = null) => {
        setActivePage(page);
        setProductId(productId);
        
        // Update URL
        let url = '/';
        if (page === 'products') url = '/products';
        else if (page === 'contact') url = '/contact';
        else if (page === 'product-detail') url = `/product/${productId}`;
        
        window.history.pushState({}, '', url);
    };

    const renderPage = () => {
        switch (activePage) {
            case 'home':
                return <HomePage />;
            case 'products':
                return <ProductsPage navigateTo={navigateTo} />;
            case 'contact':
                return <ContactPage />;
            case 'product-detail':
                return <ProductDetailPage productId={productId} navigateTo={navigateTo} />;
            default:
                return <HomePage />;
        }
    };

    return (
        <div>
            <Navigation activePage={activePage} navigateTo={navigateTo} />
            {renderPage()}
            <Footer />
        </div>
    );
};

// Render the app
ReactDOM.render(<App />, document.getElementById('root'));
