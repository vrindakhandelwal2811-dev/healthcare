from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# database
users_db = {}
moods_db = {}
journals_db = {}

# HTML TEMPLATE

BASE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qulb - Your Mental Wellness Companion</title>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&family=Comfortaa:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --soft-blue: #A7C7E7;
            --light-green: #C1E1C1;
            --lavender: #E6E6FA;
            --soft-pink: #FFE4E9;
            --cream: #FFF8F0;
            --white: #FFFFFF;
            --text-dark: #4A5568;
            --text-light: #718096;
            --gradient-1: linear-gradient(135deg, #E6E6FA 0%, #A7C7E7 50%, #C1E1C1 100%);
            --gradient-2: linear-gradient(180deg, #F0F7FF 0%, #E6E6FA 100%);
            --shadow-soft: 0 4px 20px rgba(167, 199, 231, 0.3);
            --shadow-hover: 0 8px 30px rgba(167, 199, 231, 0.4);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Quicksand', sans-serif;
            background: var(--gradient-2);
            color: var(--text-dark);
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        /* Floating Elements Animation */
        .floating-elements {
            position: fixed;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        }
        
        .leaf {
            position: absolute;
            opacity: 0.4;
            animation: float 20s infinite ease-in-out;
        }
        
        .leaf:nth-child(1) { left: 10%; animation-delay: 0s; font-size: 2rem; }
        .leaf:nth-child(2) { left: 25%; animation-delay: 3s; font-size: 1.5rem; }
        .leaf:nth-child(3) { left: 45%; animation-delay: 6s; font-size: 2.5rem; }
        .leaf:nth-child(4) { left: 65%; animation-delay: 9s; font-size: 1.8rem; }
        .leaf:nth-child(5) { left: 85%; animation-delay: 12s; font-size: 2.2rem; }
        
        @keyframes float {
            0%, 100% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
            10% { opacity: 0.4; }
            90% { opacity: 0.4; }
            100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
        }
        
        /* Navigation */
        nav {
            position: fixed;
            top: 0;
            width: 100%;
            padding: 1rem 2rem;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            z-index: 1000;
            box-shadow: 0 2px 20px rgba(167, 199, 231, 0.2);
        }
        
        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-family: 'Comfortaa', cursive;
            font-size: 1.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--soft-blue), var(--lavender));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .logo i {
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
            align-items: center;
        }
        
        .nav-links a {
            text-decoration: none;
            color: var(--text-dark);
            font-weight: 500;
            transition: all 0.3s ease;
            padding: 0.5rem 1rem;
            border-radius: 25px;
        }
        
        .nav-links a:hover {
            background: var(--lavender);
            transform: translateY(-2px);
        }
        
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 50px;
            font-family: 'Quicksand', sans-serif;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .btn-primary {
            background: var(--gradient-1);
            color: var(--text-dark);
            box-shadow: var(--shadow-soft);
        }
        
        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-hover);
        }
        
        .btn-secondary {
            background: var(--white);
            color: var(--text-dark);
            border: 2px solid var(--soft-blue);
        }
        
        .btn-secondary:hover {
            background: var(--soft-blue);
            transform: translateY(-3px);
        }
        
        /* Main Content */
        main {
            position: relative;
            z-index: 1;
            padding-top: 80px;
        }
        
        /* Hero Section */
        .hero {
            min-height: calc(100vh - 80px);
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 2rem;
            background: 
                radial-gradient(ellipse at top left, rgba(230, 230, 250, 0.5) 0%, transparent 50%),
                radial-gradient(ellipse at bottom right, rgba(193, 225, 193, 0.5) 0%, transparent 50%),
                radial-gradient(ellipse at center, rgba(167, 199, 231, 0.3) 0%, transparent 70%);
        }
        
        .hero-content {
            max-width: 800px;
            animation: fadeInUp 1s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .hero h1 {
            font-family: 'Comfortaa', cursive;
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            line-height: 1.2;
            background: linear-gradient(135deg, #5B7FA3 0%, #7B68A6 50%, #6B9B7A 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .hero p {
            font-size: 1.3rem;
            color: var(--text-light);
            margin-bottom: 2rem;
            line-height: 1.8;
        }
        
        .hero-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .hero-buttons .btn {
            padding: 1rem 2rem;
            font-size: 1.1rem;
        }
        
        /* Affirmation Banner */
        .affirmation {
            background: var(--white);
            padding: 1.5rem;
            text-align: center;
            border-top: 3px solid var(--lavender);
            border-bottom: 3px solid var(--lavender);
        }
        
        .affirmation p {
            font-family: 'Comfortaa', cursive;
            font-size: 1.3rem;
            color: var(--text-dark);
            font-style: italic;
        }
        
        .affirmation i {
            color: var(--soft-blue);
            margin: 0 0.5rem;
        }
        
        /* Features Section */
        .features {
            padding: 5rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .section-title {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .section-title h2 {
            font-family: 'Comfortaa', cursive;
            font-size: 2.5rem;
            color: var(--text-dark);
            margin-bottom: 1rem;
        }
        
        .section-title p {
            color: var(--text-light);
            font-size: 1.1rem;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
        }
        
        .feature-card {
            background: var(--white);
            padding: 2.5rem;
            border-radius: 25px;
            text-align: center;
            box-shadow: var(--shadow-soft);
            transition: all 0.4s ease;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
            display: block;
        }
        
        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: var(--shadow-hover);
        }
        
        .feature-icon {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1.5rem;
            font-size: 2rem;
        }
        
        .feature-card:nth-child(1) .feature-icon { background: linear-gradient(135deg, #A7C7E7, #87CEEB); }
        .feature-card:nth-child(2) .feature-icon { background: linear-gradient(135deg, #C1E1C1, #98D8AA); }
        .feature-card:nth-child(3) .feature-icon { background: linear-gradient(135deg, #E6E6FA, #DDA0DD); }
        .feature-card:nth-child(4) .feature-icon { background: linear-gradient(135deg, #FFE4E9, #FFB6C1); }
        
        .feature-card h3 {
            font-size: 1.3rem;
            margin-bottom: 1rem;
            color: var(--text-dark);
        }
        
        .feature-card p {
            color: var(--text-light);
            line-height: 1.6;
        }
        
        /* Mood Check Section */
        .mood-section {
            background: var(--white);
            padding: 5rem 2rem;
            text-align: center;
        }
        
        .mood-container {
            max-width: 700px;
            margin: 0 auto;
        }
        
        .mood-emojis {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            flex-wrap: wrap;
            margin-top: 2rem;
        }
        
        .mood-btn {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            border: 3px solid transparent;
            background: var(--cream);
            font-size: 2.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .mood-btn:hover {
            transform: scale(1.15);
            border-color: var(--soft-blue);
            box-shadow: var(--shadow-soft);
        }
        
        .mood-btn.selected {
            border-color: var(--light-green);
            background: var(--light-green);
            transform: scale(1.1);
        }
        
        /* Resources Section */
        .resources {
            padding: 5rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .resources-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
        }
        
        .resource-card {
            background: var(--white);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: var(--shadow-soft);
            transition: all 0.3s ease;
        }
        
        .resource-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-hover);
        }
        
        .resource-header {
            padding: 2rem;
            background: var(--gradient-1);
        }
        
        .resource-header h3 {
            color: var(--text-dark);
            font-size: 1.3rem;
        }
        
        .resource-content {
            padding: 1.5rem 2rem;
        }
        
        .resource-content p {
            color: var(--text-light);
            line-height: 1.7;
            margin-bottom: 1rem;
        }
        
        .resource-link {
            color: #7B68A6;
            text-decoration: none;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .resource-link:hover {
            text-decoration: underline;
        }
        
        /* Emergency Section */
        .emergency {
            background: linear-gradient(135deg, #FFE4E9 0%, #E6E6FA 100%);
            padding: 4rem 2rem;
            text-align: center;
            margin: 3rem 2rem;
            border-radius: 30px;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .emergency h2 {
            font-family: 'Comfortaa', cursive;
            color: var(--text-dark);
            margin-bottom: 1rem;
        }
        
        .emergency p {
            color: var(--text-light);
            margin-bottom: 2rem;
            font-size: 1.1rem;
        }
        
        .emergency-contacts {
            display: flex;
            justify-content: center;
            gap: 2rem;
            flex-wrap: wrap;
        }
        
        .emergency-contact {
            background: var(--white);
            padding: 1.5rem 2rem;
            border-radius: 15px;
            box-shadow: var(--shadow-soft);
        }
        
        .emergency-contact h4 {
            color: var(--text-dark);
            margin-bottom: 0.5rem;
        }
        
        .emergency-contact a {
            color: #E57373;
            font-size: 1.3rem;
            font-weight: 700;
            text-decoration: none;
        }
        
        /* Footer */
        footer {
            background: var(--white);
            padding: 4rem 2rem 2rem;
            margin-top: 3rem;
        }
        
        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 3rem;
        }
        
        .footer-section h4 {
            font-family: 'Comfortaa', cursive;
            margin-bottom: 1.5rem;
            color: var(--text-dark);
        }
        
        .footer-section ul {
            list-style: none;
        }
        
        .footer-section li {
            margin-bottom: 0.75rem;
        }
        
        .footer-section a {
            color: var(--text-light);
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .footer-section a:hover {
            color: var(--soft-blue);
        }
        
        .footer-bottom {
            text-align: center;
            padding-top: 3rem;
            margin-top: 3rem;
            border-top: 1px solid var(--lavender);
            color: var(--text-light);
        }
        
        /* Auth Pages */
        .auth-container {
            min-height: calc(100vh - 80px);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }
        
        .auth-card {
            background: var(--white);
            padding: 3rem;
            border-radius: 30px;
            box-shadow: var(--shadow-soft);
            width: 100%;
            max-width: 450px;
            animation: fadeInUp 0.6s ease-out;
        }
        
        .auth-card h2 {
            font-family: 'Comfortaa', cursive;
            text-align: center;
            margin-bottom: 0.5rem;
            color: var(--text-dark);
        }
        
        .auth-card .subtitle {
            text-align: center;
            color: var(--text-light);
            margin-bottom: 2rem;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            color: var(--text-dark);
            font-weight: 500;
        }
        
        .form-group input, .form-group textarea, .form-group select {
            width: 100%;
            padding: 1rem 1.25rem;
            border: 2px solid var(--lavender);
            border-radius: 15px;
            font-family: 'Quicksand', sans-serif;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: var(--white);
        }
        
        .form-group input:focus, .form-group textarea:focus, .form-group select:focus {
            outline: none;
            border-color: var(--soft-blue);
            box-shadow: 0 0 0 4px rgba(167, 199, 231, 0.2);
        }
        
        .form-group textarea {
            min-height: 150px;
            resize: vertical;
        }
        
        .auth-card .btn {
            width: 100%;
            padding: 1rem;
            font-size: 1.1rem;
            margin-top: 1rem;
        }
        
        .auth-link {
            text-align: center;
            margin-top: 1.5rem;
            color: var(--text-light);
        }
        
        .auth-link a {
            color: #7B68A6;
            text-decoration: none;
            font-weight: 600;
        }
        
        .auth-link a:hover {
            text-decoration: underline;
        }
        
        .message {
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        
        .message.error {
            background: #FFE4E9;
            color: #E57373;
        }
        
        .message.success {
            background: #C1E1C1;
            color: #4A7C59;
        }
        
        /* Dashboard */
        .dashboard {
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .welcome-banner {
            background: var(--gradient-1);
            padding: 3rem;
            border-radius: 25px;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .welcome-banner h1 {
            font-family: 'Comfortaa', cursive;
            color: var(--text-dark);
            margin-bottom: 0.5rem;
        }
        
        .welcome-banner p {
            color: var(--text-light);
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
        }
        
        .dashboard-card {
            background: var(--white);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: var(--shadow-soft);
        }
        
        .dashboard-card h3 {
            font-family: 'Comfortaa', cursive;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            color: var(--text-dark);
        }
        
        .dashboard-card h3 i {
            color: var(--soft-blue);
        }
        
        /* Journal Entries */
        .journal-entries {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .journal-entry {
            background: var(--cream);
            padding: 1.25rem;
            border-radius: 15px;
            margin-bottom: 1rem;
        }
        
        .journal-entry .date {
            font-size: 0.85rem;
            color: var(--text-light);
            margin-bottom: 0.5rem;
        }
        
        .journal-entry .content {
            color: var(--text-dark);
            line-height: 1.6;
        }
        
        /* Mood History */
        .mood-history {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
        }
        
        .mood-item {
            background: var(--cream);
            padding: 0.75rem 1rem;
            border-radius: 10px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
        }
        
        .mood-item .emoji {
            font-size: 1.5rem;
        }
        
        /* Meditation Player */
        .meditation-card {
            background: linear-gradient(135deg, var(--soft-blue) 0%, var(--lavender) 100%);
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            color: var(--text-dark);
        }
        
        .meditation-card h4 {
            margin-bottom: 1rem;
        }
        
        .play-btn {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: var(--white);
            border: none;
            font-size: 2rem;
            color: var(--soft-blue);
            cursor: pointer;
            margin: 1.5rem 0;
            transition: all 0.3s ease;
            box-shadow: var(--shadow-soft);
        }
        
        .play-btn:hover {
            transform: scale(1.1);
            box-shadow: var(--shadow-hover);
        }
        
        /* Quick Actions */
        .quick-actions {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }
        
        .quick-action {
            background: var(--cream);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            text-decoration: none;
            color: var(--text-dark);
            transition: all 0.3s ease;
        }
        
        .quick-action:hover {
            background: var(--lavender);
            transform: translateY(-3px);
        }
        
        .quick-action i {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
            color: var(--soft-blue);
        }
        
        .quick-action span {
            display: block;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        /* Mobile Menu */
        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            font-size: 1.5rem;
            color: var(--text-dark);
            cursor: pointer;
        }
        
        @media (max-width: 768px) {
            .mobile-menu-btn {
                display: block;
            }
            
            .nav-links {
                display: none;
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: var(--white);
                padding: 1rem;
                flex-direction: column;
                gap: 0.5rem;
                box-shadow: var(--shadow-soft);
            }
            
            .nav-links.active {
                display: flex;
            }
            
            .hero h1 {
                font-size: 2.2rem;
            }
            
            .hero p {
                font-size: 1.1rem;
            }
            
            .features-grid, .resources-grid, .dashboard-grid {
                grid-template-columns: 1fr;
            }
            
            .mood-emojis {
                gap: 1rem;
            }
            
            .mood-btn {
                width: 60px;
                height: 60px;
                font-size: 2rem;
            }
        }
        
        /* Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--cream);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--soft-blue);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--lavender);
        }
    </style>
</head>
<body>
    <!-- Floating Nature Elements -->
    <div class="floating-elements">
        <div class="leaf">🍃</div>
        <div class="leaf">🌿</div>
        <div class="leaf">☁️</div>
        <div class="leaf">🍂</div>
        <div class="leaf">🌸</div>
    </div>
    
    <!-- Navigation -->
    <nav>
        <div class="nav-container">
            <a href="/" class="logo">
                <i class="fas fa-heart"></i>
                Qulb
            </a>
            <button class="mobile-menu-btn" onclick="toggleMenu()">
                <i class="fas fa-bars"></i>
            </button>
            <div class="nav-links" id="navLinks">
                <a href="/">Home</a>
                <a href="/resources">Resources</a>
                <a href="/meditation">Meditation</a>
                {% if session.get('user') %}
                    <a href="/dashboard">Dashboard</a>
                    <a href="/journal">Journal</a>
                    <a href="/logout" class="btn btn-secondary">Logout</a>
                {% else %}
                    <a href="/login" class="btn btn-secondary">Sign In</a>
                    <a href="/register" class="btn btn-primary">Get Started</a>
                {% endif %}
            </div>
        </div>
    </nav>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    <footer>
        <div class="footer-content">
            <div class="footer-section">
                <h4>🌿 Qulb</h4>
                <p style="color: var(--text-light); line-height: 1.6;">
                    A safe space for your mental wellness journey. You are not alone.
                </p>
            </div>
            <div class="footer-section">
                <h4>Resources</h4>
                <ul>
                    <li><a href="/resources">Self-Help Articles</a></li>
                    <li><a href="/meditation">Meditation</a></li>
                    <li><a href="#">Therapist Directory</a></li>
                    <li><a href="#">Community</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h4>Support</h4>
                <ul>
                    <li><a href="#">About Us</a></li>
                    <li><a href="#">Contact</a></li>
                    <li><a href="#">Privacy Policy</a></li>
                    <li><a href="#">Terms of Service</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h4>Helplines</h4>
                <ul>
                    <li><a href="tel:18005990019">KIRAN: 1800-599-0019</a></li>
                    <li><a href="tel:9152987821">iCall: 9152987821</a></li>
                    <li><a href="tel:18602662345">Vandrevala: 1860-266-2345</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p>💜 Made with love for those who need it most</p>
            <p style="margin-top: 0.5rem;">© Qulb. All rights reserved.</p>
        </div>
    </footer>
    
    <script>
        function toggleMenu() {
            document.getElementById('navLinks').classList.toggle('active');
        }
    </script>
</body>
</html>
'''

HOME_TEMPLATE = '''
{% extends "base" %}
{% block content %}
    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-content">
            <h1>You're not alone.<br>We're here for you. 💜</h1>
            <p>
                A gentle space where you can breathe, reflect, and find support. 
                Your mental health matters, and it's okay to ask for help.
            </p>
            <div class="hero-buttons">
                {% if session.get('user') %}
                    <a href="/dashboard" class="btn btn-primary">
                        <i class="fas fa-home"></i> Go to Dashboard
                    </a>
                {% else %}
                    <a href="/register" class="btn btn-primary">
                        <i class="fas fa-heart"></i> Get Support
                    </a>
                    <a href="/resources" class="btn btn-secondary">
                        <i class="fas fa-book-open"></i> Explore Resources
                    </a>
                {% endif %}
            </div>
        </div>
    </section>
    
    <!-- Affirmation Banner -->
    <div class="affirmation">
        <p><i class="fas fa-quote-left"></i> You are enough. This feeling will pass. <i class="fas fa-quote-right"></i></p>
    </div>
    
    <!-- Features Section -->
    <section class="features">
        <div class="section-title">
            <h2>How We Can Help 🌸</h2>
            <p>Tools and resources designed with your wellbeing in mind</p>
        </div>
        <div class="features-grid">
            <a href="{% if session.get('user') %}/dashboard{% else %}/register{% endif %}" class="feature-card">
                <div class="feature-icon">🧠</div>
                <h3>Mood Tracker</h3>
                <p>Track your emotional patterns over time and gain insights into your mental wellness journey.</p>
            </a>
            <a href="{% if session.get('user') %}/journal{% else %}/register{% endif %}" class="feature-card">
                <div class="feature-icon">💬</div>
                <h3>Private Journal</h3>
                <p>A safe space to express your thoughts and feelings without judgment.</p>
            </a>
            <a href="/resources" class="feature-card">
                <div class="feature-icon">📖</div>
                <h3>Self-Help Resources</h3>
                <p>Articles, guides, and exercises to support your mental health.</p>
            </a>
            <a href="/meditation" class="feature-card">
                <div class="feature-icon">🧘</div>
                <h3>Meditation & Relaxation</h3>
                <p>Guided sessions to help you find calm and inner peace.</p>
            </a>
        </div>
    </section>
    
    <!-- Mood Check Section -->
    <section class="mood-section">
        <div class="mood-container">
            <div class="section-title">
                <h2>How are you feeling today? 🌤️</h2>
                <p>It's okay to feel however you're feeling right now</p>
            </div>
            <div class="mood-emojis">
                <button class="mood-btn" onclick="selectMood('😊', 'Great')" title="Great">😊</button>
                <button class="mood-btn" onclick="selectMood('🙂', 'Good')" title="Good">🙂</button>
                <button class="mood-btn" onclick="selectMood('😐', 'Okay')" title="Okay">😐</button>
                <button class="mood-btn" onclick="selectMood('😔', 'Sad')" title="Sad">😔</button>
                <button class="mood-btn" onclick="selectMood('😢', 'Struggling')" title="Struggling">😢</button>
            </div>
            <div id="moodResponse" style="margin-top: 2rem; display: none;">
                <p id="moodMessage" style="font-size: 1.2rem; color: var(--text-dark);"></p>
            </div>
        </div>
    </section>
    
    <!-- Resources Section -->
    <section class="resources">
        <div class="section-title">
            <h2>Helpful Resources 📚</h2>
            <p>Knowledge is a powerful tool for healing</p>
        </div>
        <div class="resources-grid">
            <div class="resource-card">
                <div class="resource-header">
                    <h3>🌊 Managing Anxiety</h3>
                </div>
                <div class="resource-content">
                    <p>Learn practical techniques to calm your mind when anxiety feels overwhelming. Includes breathing exercises and grounding techniques.</p>
                    <a href="/resources" class="resource-link">Read More <i class="fas fa-arrow-right"></i></a>
                </div>
            </div>
            <div class="resource-card">
                <div class="resource-header">
                    <h3>💪 Building Resilience</h3>
                </div>
                <div class="resource-content">
                    <p>Discover ways to strengthen your emotional resilience and bounce back from difficult times with renewed strength.</p>
                    <a href="/resources" class="resource-link">Read More <i class="fas fa-arrow-right"></i></a>
                </div>
            </div>
            <div class="resource-card">
                <div class="resource-header">
                    <h3>😴 Better Sleep</h3>
                </div>
                <div class="resource-content">
                    <p>Tips and techniques for improving your sleep quality, which is essential for mental and emotional wellbeing.</p>
                    <a href="/resources" class="resource-link">Read More <i class="fas fa-arrow-right"></i></a>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Emergency Section -->
    <section class="emergency">
        <h2>🆘 Need Immediate Help?</h2>
        <p>If you're in crisis or having thoughts of self-harm, please reach out. Help is available 24/7.</p>
        <div class="emergency-contacts">
            <div class="emergency-contact">
                <h4>KIRAN Helpline</h4>
                <a href="tel:18005990019">1800-599-0019</a>
            </div>
            <div class="emergency-contact">
                <h4>iCall Helpline</h4>
                <a href="tel:9152987821">9152987821</a>
            </div>
            <div class="emergency-contact">
                <h4>Vandrevala Foundation</h4>
                <a href="tel:18602662345">1860-266-2345</a>
            </div>
        </div>
    </section>
    
    <script>
        const moodMessages = {
            'Great': "🌟 That's wonderful! Keep nurturing what brings you joy!",
            'Good': "💚 Nice to hear! Remember to appreciate these good moments.",
            'Okay': "🌿 It's perfectly fine to feel neutral. Take things one step at a time.",
            'Sad': "💜 We're sorry you're feeling down. Remember, it's okay to not be okay. Consider journaling or talking to someone.",
            'Struggling': "🫂 We hear you. Please know that you matter and support is available. Would you like to explore our resources or talk to someone?"
        };
        
        function selectMood(emoji, mood) {
            document.querySelectorAll('.mood-btn').forEach(btn => btn.classList.remove('selected'));
            event.target.classList.add('selected');
            
            document.getElementById('moodMessage').textContent = moodMessages[mood];
            document.getElementById('moodResponse').style.display = 'block';
            
            // If logged in, save mood via API
            fetch('/api/mood', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ emoji: emoji, mood: mood })
            });
        }
    </script>
{% endblock %}
'''

LOGIN_TEMPLATE = '''
{% extends "base" %}
{% block content %}
    <div class="auth-container">
        <div class="auth-card">
            <h2>Welcome Back 💜</h2>
            <p class="subtitle">Sign in to continue your wellness journey</p>
            
            {% if error %}
                <div class="message error">{{ error }}</div>
            {% endif %}
            
            <form method="POST">
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" placeholder="your@email.com" required>
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" placeholder="Your password" required>
                </div>
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-sign-in-alt"></i> Sign In
                </button>
            </form>
            
            <p class="auth-link">
                New here? <a href="/register">Create an account</a>
            </p>
        </div>
    </div>
{% endblock %}
'''

REGISTER_TEMPLATE = '''
{% extends "base" %}
{% block content %}
    <div class="auth-container">
        <div class="auth-card">
            <h2>Join Qulb 🌿</h2>
            <p class="subtitle">Start your wellness journey today</p>
            
            {% if error %}
                <div class="message error">{{ error }}</div>
            {% endif %}
            
            <form method="POST">
                <div class="form-group">
                    <label for="name">Your Name</label>
                    <input type="text" id="name" name="name" placeholder="How should we call you?" required>
                </div>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" placeholder="your@email.com" required>
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" placeholder="Create a password" required minlength="6">
                </div>
                <div class="form-group">
                    <label for="confirm_password">Confirm Password</label>
                    <input type="password" id="confirm_password" name="confirm_password" placeholder="Confirm your password" required>
                </div>
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-heart"></i> Create Account
                </button>
            </form>
            
            <p class="auth-link">
                Already have an account? <a href="/login">Sign in</a>
            </p>
        </div>
    </div>
{% endblock %}
'''

DASHBOARD_TEMPLATE = '''
{% extends "base" %}
{% block content %}
    <div class="dashboard">
        <div class="welcome-banner">
            <h1>Welcome back, {{ session.get('name', 'Friend') }}! 🌸</h1>
            <p>How are you feeling today? Remember, every small step counts.</p>
        </div>
        
        <div class="dashboard-grid">
            <!-- Mood Tracker Card -->
            <div class="dashboard-card">
                <h3><i class="fas fa-smile"></i> Today's Mood Check</h3>
                <p style="color: var(--text-light); margin-bottom: 1rem;">How are you feeling right now?</p>
                <div class="mood-emojis" style="justify-content: flex-start; gap: 0.75rem;">
                    <button class="mood-btn" style="width: 55px; height: 55px; font-size: 1.8rem;" onclick="saveMood('😊', 'Great')">😊</button>
                    <button class="mood-btn" style="width: 55px; height: 55px; font-size: 1.8rem;" onclick="saveMood('🙂', 'Good')">🙂</button>
                    <button class="mood-btn" style="width: 55px; height: 55px; font-size: 1.8rem;" onclick="saveMood('😐', 'Okay')">😐</button>
                    <button class="mood-btn" style="width: 55px; height: 55px; font-size: 1.8rem;" onclick="saveMood('😔', 'Sad')">😔</button>
                    <button class="mood-btn" style="width: 55px; height: 55px; font-size: 1.8rem;" onclick="saveMood('😢', 'Struggling')">😢</button>
                </div>
                <div id="moodSaved" style="margin-top: 1rem; display: none; color: var(--light-green);">
                    <i class="fas fa-check-circle"></i> Mood saved!
                </div>
                
                <h4 style="margin-top: 2rem; margin-bottom: 1rem; color: var(--text-dark);">Recent Moods</h4>
                <div class="mood-history">
                    {% for mood in moods[-7:] %}
                        <div class="mood-item">
                            <span class="emoji">{{ mood.emoji }}</span>
                            <span>{{ mood.date }}</span>
                        </div>
                    {% else %}
                        <p style="color: var(--text-light);">No moods recorded yet. Start tracking above!</p>
                    {% endfor %}
                </div>
            </div>
            
            <!-- Quick Actions -->
            <div class="dashboard-card">
                <h3><i class="fas fa-bolt"></i> Quick Actions</h3>
                <div class="quick-actions">
                    <a href="/journal" class="quick-action">
                        <i class="fas fa-pen"></i>
                        <span>Write Journal</span>
                    </a>
                    <a href="/meditation" class="quick-action">
                        <i class="fas fa-spa"></i>
                        <span>Meditate</span>
                    </a>
                    <a href="/resources" class="quick-action">
                        <i class="fas fa-book"></i>
                        <span>Resources</span>
                    </a>
                    <a href="#" class="quick-action" onclick="showBreathingExercise()">
                        <i class="fas fa-wind"></i>
                        <span>Breathe</span>
                    </a>
                </div>
                
                <!-- Mini Meditation -->
                <div class="meditation-card" style="margin-top: 1.5rem;">
                    <h4>🧘 Quick Relaxation</h4>
                    <p style="font-size: 0.9rem; margin-bottom: 1rem;">Take a moment to breathe</p>
                    <button class="play-btn" onclick="startBreathing()">
                        <i class="fas fa-play"></i>
                    </button>
                    <p id="breathingText" style="font-size: 1.1rem;">Press play to begin</p>
                </div>
            </div>
            
            <!-- Recent Journal Entries -->
            <div class="dashboard-card">
                <h3><i class="fas fa-book-open"></i> Recent Journal Entries</h3>
                <div class="journal-entries">
                    {% for entry in journals[-5:] %}
                        <div class="journal-entry">
                            <div class="date">{{ entry.date }}</div>
                            <div class="content">{{ entry.content[:200] }}{% if entry.content|length > 200 %}...{% endif %}</div>
                        </div>
                    {% else %}
                        <p style="color: var(--text-light);">No journal entries yet. <a href="/journal">Start writing</a></p>
                    {% endfor %}
                </div>
                <a href="/journal" class="btn btn-secondary" style="margin-top: 1rem;">
                    <i class="fas fa-plus"></i> New Entry
                </a>
            </div>
            
            <!-- Daily Affirmation -->
            <div class="dashboard-card" style="background: var(--gradient-1);">
                <h3 style="color: var(--text-dark);"><i class="fas fa-heart"></i> Today's Affirmation</h3>
                <p style="font-size: 1.3rem; font-style: italic; line-height: 1.8; color: var(--text-dark);" id="affirmation">
                    Loading...
                </p>
                <button onclick="newAffirmation()" class="btn btn-secondary" style="margin-top: 1rem;">
                    <i class="fas fa-sync-alt"></i> New Affirmation
                </button>
            </div>
        </div>
    </div>
    
    <script>
        const affirmations = [
            "You are worthy of love and kindness, especially from yourself. 💜",
            "Every small step forward is progress worth celebrating. 🌟",
            "Your feelings are valid, and it's okay to feel them fully. 🌊",
            "You are stronger than you know and braver than you believe. 💪",
            "This moment of struggle is not your forever. Better days are coming. 🌅",
            "You deserve peace, happiness, and all good things. 🌸",
            "It's okay to rest. You don't have to earn your break. 🍃",
            "You are enough, exactly as you are right now. ✨",
            "Your presence makes the world a better place. 🌍",
            "Healing is not linear, and that's perfectly okay. 🌈"
        ];
        
        function newAffirmation() {
            const affirmation = affirmations[Math.floor(Math.random() * affirmations.length)];
            document.getElementById('affirmation').textContent = affirmation;
        }
        
        newAffirmation();
        
        function saveMood(emoji, mood) {
            fetch('/api/mood', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ emoji: emoji, mood: mood })
            }).then(() => {
                document.getElementById('moodSaved').style.display = 'block';
                setTimeout(() => location.reload(), 1000);
            });
        }
        
        let breathingInterval;
        let isBreathing = false;
        
        function startBreathing() {
            const textEl = document.getElementById('breathingText');
            const btn = document.querySelector('.play-btn');
            
            if (isBreathing) {
                clearInterval(breathingInterval);
                textEl.textContent = 'Press play to begin';
                btn.innerHTML = '<i class="fas fa-play"></i>';
                isBreathing = false;
                return;
            }
            
            isBreathing = true;
            btn.innerHTML = '<i class="fas fa-pause"></i>';
            
            const phases = [
                { text: 'Breathe in... 🌬️', duration: 4000 },
                { text: 'Hold... 💜', duration: 4000 },
                { text: 'Breathe out... 🍃', duration: 4000 },
                { text: 'Hold... ✨', duration: 4000 }
            ];
            
            let phaseIndex = 0;
            
            function nextPhase() {
                textEl.textContent = phases[phaseIndex].text;
                phaseIndex = (phaseIndex + 1) % phases.length;
            }
            
            nextPhase();
            breathingInterval = setInterval(() => {
                nextPhase();
            }, 4000);
        }
    </script>
{% endblock %}
'''

JOURNAL_TEMPLATE = '''
{% extends "base" %}
{% block content %}
    <div class="dashboard">
        <div class="welcome-banner">
            <h1>Your Private Journal 📝</h1>
            <p>A safe space to express your thoughts and feelings</p>
        </div>
        
        <div class="dashboard-grid">
            <!-- New Entry Form -->
            <div class="dashboard-card">
                <h3><i class="fas fa-pen-fancy"></i> New Entry</h3>
                
                {% if success %}
                    <div class="message success">{{ success }}</div>
                {% endif %}
                
                <form method="POST">
                    <div class="form-group">
                        <label for="mood">How are you feeling?</label>
                        <select id="mood" name="mood">
                            <option value="😊 Great">😊 Great</option>
                            <option value="🙂 Good">🙂 Good</option>
                            <option value="😐 Okay" selected>😐 Okay</option>
                            <option value="😔 Sad">😔 Sad</option>
                            <option value="😢 Struggling">😢 Struggling</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="content">What's on your mind?</label>
                        <textarea id="content" name="content" placeholder="Write freely... This is your safe space. No one else can see this." required></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-save"></i> Save Entry
                    </button>
                </form>
                
                <!-- Writing Prompts -->
                <div style="margin-top: 2rem; padding: 1.5rem; background: var(--cream); border-radius: 15px;">
                    <h4 style="margin-bottom: 1rem; color: var(--text-dark);">💡 Writing Prompts</h4>
                    <ul style="color: var(--text-light); line-height: 2;">
                        <li>What am I grateful for today?</li>
                        <li>What made me smile recently?</li>
                        <li>What's one thing I'm proud of?</li>
                        <li>What do I need to let go of?</li>
                        <li>How can I be kinder to myself?</li>
                    </ul>
                </div>
            </div>
            
            <!-- Past Entries -->
            <div class="dashboard-card">
                <h3><i class="fas fa-history"></i> Past Entries</h3>
                <div class="journal-entries" style="max-height: 600px;">
                    {% for entry in journals|reverse %}
                        <div class="journal-entry">
                            <div class="date" style="display: flex; justify-content: space-between; align-items: center;">
                                <span>{{ entry.date }}</span>
                                <span>{{ entry.mood }}</span>
                            </div>
                            <div class="content">{{ entry.content }}</div>
                        </div>
                    {% else %}
                        <div style="text-align: center; padding: 3rem; color: var(--text-light);">
                            <i class="fas fa-book-open" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                            <p>Your journal is empty. Start writing your first entry!</p>
                        </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
{% endblock %}
'''

MEDITATION_TEMPLATE = '''
{% extends "base" %}
{% block content %}
    <div class="dashboard">
        <div class="welcome-banner">
            <h1>Meditation & Relaxation 🧘</h1>
            <p>Find your calm with guided exercises</p>
        </div>
        
        <div class="dashboard-grid">
            <!-- Breathing Exercise -->
            <div class="dashboard-card" style="text-align: center;">
                <h3><i class="fas fa-wind"></i> Breathing Exercise</h3>
                <p style="color: var(--text-light); margin-bottom: 2rem;">Follow the circle to calm your nervous system</p>
                
                <div id="breathingCircle" style="
                    width: 200px;
                    height: 200px;
                    border-radius: 50%;
                    background: var(--gradient-1);
                    margin: 2rem auto;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.3rem;
                    color: var(--text-dark);
                    transition: transform 4s ease-in-out;
                ">
                    Press Start
                </div>
                
                <button onclick="toggleBreathing()" class="btn btn-primary" id="breathBtn">
                    <i class="fas fa-play"></i> Start Breathing
                </button>
            </div>
            
            <!-- Guided Meditations -->
            <div class="dashboard-card">
                <h3><i class="fas fa-spa"></i> Guided Sessions</h3>
                
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    <div class="meditation-item" style="background: var(--cream); padding: 1.5rem; border-radius: 15px; cursor: pointer;" onclick="playMeditation('morning')">
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <div style="width: 50px; height: 50px; border-radius: 50%; background: linear-gradient(135deg, #FFE4B5, #FFA500); display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">
                                🌅
                            </div>
                            <div>
                                <h4 style="color: var(--text-dark);">Morning Calm</h4>
                                <p style="color: var(--text-light); font-size: 0.9rem;">5 min • Start your day peacefully</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="meditation-item" style="background: var(--cream); padding: 1.5rem; border-radius: 15px; cursor: pointer;" onclick="playMeditation('anxiety')">
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <div style="width: 50px; height: 50px; border-radius: 50%; background: linear-gradient(135deg, #A7C7E7, #87CEEB); display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">
                                🌊
                            </div>
                            <div>
                                <h4 style="color: var(--text-dark);">Anxiety Relief</h4>
                                <p style="color: var(--text-light); font-size: 0.9rem;">10 min • Find your center</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="meditation-item" style="background: var(--cream); padding: 1.5rem; border-radius: 15px; cursor: pointer;" onclick="playMeditation('sleep')">
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <div style="width: 50px; height: 50px; border-radius: 50%; background: linear-gradient(135deg, #E6E6FA, #9370DB); display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">
                                🌙
                            </div>
                            <div>
                                <h4 style="color: var(--text-dark);">Sleep Well</h4>
                                <p style="color: var(--text-light); font-size: 0.9rem;">15 min • Drift into peaceful sleep</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="meditation-item" style="background: var(--cream); padding: 1.5rem; border-radius: 15px; cursor: pointer;" onclick="playMeditation('gratitude')">
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <div style="width: 50px; height: 50px; border-radius: 50%; background: linear-gradient(135deg, #C1E1C1, #98D8AA); display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">
                                💚
                            </div>
                            <div>
                                <h4 style="color: var(--text-dark);">Gratitude Practice</h4>
                                <p style="color: var(--text-light); font-size: 0.9rem;">7 min • Cultivate appreciation</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Calming Sounds -->
            <div class="dashboard-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3><i class="fas fa-music"></i> Calming Sounds</h3>
                    <button onclick="stopAllSounds()" class="btn-text" style="color: var(--text-light); text-decoration: underline;">Stop All</button>
                </div>
                <p style="color: var(--text-light); margin-bottom: 1.5rem;">Background sounds to help you relax</p>
                
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
                    <button class="sound-btn" data-sound="rain" style="padding: 1.5rem; border: 2px solid var(--lavender); background: var(--white); border-radius: 15px; cursor: pointer; transition: all 0.3s ease;" onclick="toggleSound(this, 'rain')">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌧️</div>
                        <span style="color: var(--text-dark);">Rain</span>
                    </button>
                    <button class="sound-btn" data-sound="ocean" style="padding: 1.5rem; border: 2px solid var(--lavender); background: var(--white); border-radius: 15px; cursor: pointer; transition: all 0.3s ease;" onclick="toggleSound(this, 'ocean')">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌊</div>
                        <span style="color: var(--text-dark);">Ocean</span>
                    </button>
                    <button class="sound-btn" data-sound="forest" style="padding: 1.5rem; border: 2px solid var(--lavender); background: var(--white); border-radius: 15px; cursor: pointer; transition: all 0.3s ease;" onclick="toggleSound(this, 'forest')">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌲</div>
                        <span style="color: var(--text-dark);">Forest</span>
                    </button>
                    <button class="sound-btn" data-sound="fireplace" style="padding: 1.5rem; border: 2px solid var(--lavender); background: var(--white); border-radius: 15px; cursor: pointer; transition: all 0.3s ease;" onclick="toggleSound(this, 'fireplace')">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔥</div>
                        <span style="color: var(--text-dark);">Fireplace</span>
                    </button>
                </div>
                <div style="margin-top: 1.5rem;">
                    <label style="display: block; color: var(--text-dark); margin-bottom: 0.5rem;">Volume</label>
                    <input type="range" id="soundVolume" min="0" max="1" step="0.05" value="0.3" style="width: 100%;" oninput="setSoundVolume(this.value)">
                </div>
            </div>
            
            <!-- Body Scan -->
            <div class="dashboard-card" style="background: linear-gradient(135deg, var(--soft-pink) 0%, var(--lavender) 100%);">
                <h3 style="color: var(--text-dark);"><i class="fas fa-child"></i> Body Scan Relaxation</h3>
                <p style="color: var(--text-dark); margin-bottom: 1.5rem;">Release tension from head to toe</p>
                
                <div id="bodyScan" style="text-align: center; padding: 2rem;">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">🧘</div>
                    <p id="bodyScanText" style="font-size: 1.2rem; color: var(--text-dark);">Press start to begin the body scan</p>
                </div>
                
                <button onclick="startBodyScan()" class="btn btn-secondary" id="bodyScanBtn">
                    <i class="fas fa-play"></i> Start Body Scan
                </button>
            </div>
        </div>
    </div>
    
    <script>
        (function(){
            "use strict";
            
            // ----- Audio Engine (Web Audio API) -----
            let audioContext = null;
            let masterGain = null;
            let currentSound = null;       // { source, gain, type, button }
            
            // Initialize audio context on first user interaction
            async function initAudio() {
                if (audioContext) {
                    if (audioContext.state === 'suspended') {
                        await audioContext.resume();
                    }
                    return;
                }
                try {
                    audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    masterGain = audioContext.createGain();
                    masterGain.gain.value = 0.3;
                    masterGain.connect(audioContext.destination);
                } catch(e) {
                    console.warn('Web Audio API not supported');
                }
            }
            
            // Stop currently playing sound and clean up
            function stopCurrentSound() {
                if (currentSound) {
                    try {
                        if (currentSound.source) {
                            currentSound.source.stop();
                            currentSound.source.disconnect();
                        }
                        if (currentSound.gain) currentSound.gain.disconnect();
                    } catch(e) {}
                    
                    // Reset button style
                    if (currentSound.button) {
                        currentSound.button.style.background = 'var(--white)';
                    }
                    currentSound = null;
                }
            }
            
            // Set master volume
            window.setSoundVolume = function(value) {
                const vol = parseFloat(value);
                if (masterGain) {
                    masterGain.gain.value = vol;
                }
            };
            
            // Stop all sounds (including speech)
            window.stopAllSounds = function() {
                stopCurrentSound();
                stopSpeech();
                if (audioContext && audioContext.state === 'running') {
                    // Don't close, just suspend to save resources
                    audioContext.suspend();
                }
                // Reset all sound button styles
                document.querySelectorAll('.sound-btn').forEach(btn => {
                    btn.style.background = 'var(--white)';
                });
            };
            
            // Generate noise buffer (white noise)
            function createNoiseBuffer(duration = 2) {
                const sampleRate = audioContext.sampleRate;
                const bufferSize = duration * sampleRate;
                const buffer = audioContext.createBuffer(1, bufferSize, sampleRate);
                const data = buffer.getChannelData(0);
                for (let i = 0; i < bufferSize; i++) {
                    data[i] = Math.random() * 2 - 1;
                }
                return buffer;
            }
            
            // Create rain sound (filtered noise)
            function createRainSound() {
                const buffer = createNoiseBuffer(2);
                const source = audioContext.createBufferSource();
                source.buffer = buffer;
                source.loop = true;
                
                // Low-pass filter for rain texture
                const filter = audioContext.createBiquadFilter();
                filter.type = 'lowpass';
                filter.frequency.value = 800;
                
                const gain = audioContext.createGain();
                gain.gain.value = 0.4;
                
                source.connect(filter);
                filter.connect(gain);
                gain.connect(masterGain);
                
                return { source, gain };
            }
            
            // Create ocean waves (modulated noise)
            function createOceanSound() {
                const buffer = createNoiseBuffer(2);
                const source = audioContext.createBufferSource();
                source.buffer = buffer;
                source.loop = true;
                
                const filter = audioContext.createBiquadFilter();
                filter.type = 'lowpass';
                filter.frequency.value = 400;
                
                // LFO to modulate volume for wave effect
                const lfo = audioContext.createOscillator();
                lfo.frequency.value = 0.15;
                const lfoGain = audioContext.createGain();
                lfoGain.gain.value = 0.3;
                
                const gain = audioContext.createGain();
                gain.gain.value = 0.5;
                
                lfo.connect(lfoGain);
                lfoGain.connect(gain.gain);
                
                source.connect(filter);
                filter.connect(gain);
                gain.connect(masterGain);
                
                lfo.start();
                
                return { source, gain, lfo };
            }
            
            // Create forest sound (wind + occasional birds)
            function createForestSound() {
                // Wind noise
                const windBuffer = createNoiseBuffer(2);
                const windSource = audioContext.createBufferSource();
                windSource.buffer = windBuffer;
                windSource.loop = true;
                
                const windFilter = audioContext.createBiquadFilter();
                windFilter.type = 'lowpass';
                windFilter.frequency.value = 600;
                
                const windGain = audioContext.createGain();
                windGain.gain.value = 0.3;
                
                windSource.connect(windFilter);
                windFilter.connect(windGain);
                windGain.connect(masterGain);
                
                // Bird chirps (simple oscillator bursts)
                const birdGain = audioContext.createGain();
                birdGain.gain.value = 0.15;
                birdGain.connect(masterGain);
                
                let birdInterval;
                const scheduleBird = () => {
                    if (!currentSound || currentSound.type !== 'forest') return;
                    const now = audioContext.currentTime;
                    const osc = audioContext.createOscillator();
                    osc.type = 'sine';
                    osc.frequency.value = 1800 + Math.random() * 1200;
                    const env = audioContext.createGain();
                    env.gain.setValueAtTime(0, now);
                    env.gain.linearRampToValueAtTime(0.3, now + 0.02);
                    env.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
                    osc.connect(env);
                    env.connect(birdGain);
                    osc.start(now);
                    osc.stop(now + 0.2);
                };
                
                birdInterval = setInterval(scheduleBird, 4000);
                
                // Return with cleanup
                return { 
                    source: windSource, 
                    gain: windGain, 
                    extraSources: [windSource],
                    cleanup: () => clearInterval(birdInterval)
                };
            }
            
            // Create fireplace sound (crackling noise)
            function createFireplaceSound() {
                const bufferSize = 2 * audioContext.sampleRate;
                const buffer = audioContext.createBuffer(1, bufferSize, audioContext.sampleRate);
                const data = buffer.getChannelData(0);
                
                for (let i = 0; i < bufferSize; i++) {
                    let sample = (Math.random() * 2 - 1) * 0.15;
                    // Random crackles
                    if (Math.random() < 0.005) {
                        const intensity = Math.random() * 0.6;
                        const decay = Math.exp(- (i % 2000) / 500);
                        sample += (Math.random() * 2 - 1) * intensity * decay;
                    }
                    data[i] = sample;
                }
                
                const source = audioContext.createBufferSource();
                source.buffer = buffer;
                source.loop = true;
                
                const filter = audioContext.createBiquadFilter();
                filter.type = 'lowpass';
                filter.frequency.value = 1500;
                
                const gain = audioContext.createGain();
                gain.gain.value = 0.4;
                
                source.connect(filter);
                filter.connect(gain);
                gain.connect(masterGain);
                
                return { source, gain };
            }
            
            // Toggle ambient sound
            window.toggleSound = async function(btn, soundType) {
                await initAudio();
                
                // If same sound is playing, stop it
                if (currentSound && currentSound.type === soundType) {
                    stopCurrentSound();
                    return;
                }
                
                // Stop any existing sound
                stopCurrentSound();
                
                // Create new sound
                let soundComponents;
                switch(soundType) {
                    case 'rain':
                        soundComponents = createRainSound();
                        break;
                    case 'ocean':
                        soundComponents = createOceanSound();
                        break;
                    case 'forest':
                        soundComponents = createForestSound();
                        break;
                    case 'fireplace':
                        soundComponents = createFireplaceSound();
                        break;
                    default:
                        return;
                }
                
                const { source, gain, lfo, cleanup } = soundComponents;
                
                source.start();
                if (lfo) lfo.start();
                
                currentSound = {
                    source,
                    gain,
                    lfo,
                    cleanup,
                    type: soundType,
                    button: btn
                };
                
                // Highlight button
                btn.style.background = 'var(--gradient-1)';
                
                // Resume context if suspended
                if (audioContext.state === 'suspended') {
                    await audioContext.resume();
                }
            };
            
            // ----- Speech Synthesis (Guided Meditations) -----
            let speechUtterance = null;
            let speechActive = false;
            
            function stopSpeech() {
                if (window.speechSynthesis) {
                    window.speechSynthesis.cancel();
                }
                speechActive = false;
                speechUtterance = null;
            }
            
            // Preload voices for better performance
            function loadVoices() {
                return new Promise((resolve) => {
                    let voices = window.speechSynthesis.getVoices();
                    if (voices.length) {
                        resolve(voices);
                    } else {
                        window.speechSynthesis.addEventListener('voiceschanged', () => {
                            resolve(window.speechSynthesis.getVoices());
                        }, { once: true });
                    }
                });
            }
            
            window.playMeditation = async function(type) {
                stopSpeech();
                speechActive = true;
                
                const scripts = {
                    morning: "Welcome to Morning Calm. Find a comfortable seat. Close your eyes gently. Take a deep breath in... and out. Notice the morning light behind your eyelids. Set an intention for your day: may I be peaceful, may I be kind. Breathe in possibility, breathe out any tension. Continue this gentle breathing for a few moments. When you're ready, slowly open your eyes. Carry this calm with you throughout your day.",
                    anxiety: "This is Anxiety Relief meditation. Find a comfortable position. Bring your attention to your breath. Notice where you feel anxiety in your body. Breathe into that area with kindness. Imagine a wave of calm washing over you with each exhale. You are safe in this moment. This feeling will pass. Repeat silently: I am okay, I am breathing, I am here. Continue for a few more breaths.",
                    sleep: "Sleep Well meditation. Lie down and close your eyes. Release the day's worries. Scan your body from head to toe, relaxing each part. Imagine a soft, warm blanket of peace covering you. Your mind is quiet, your body heavy and relaxed. Drift deeper with each breath. You deserve rest. Sleep now.",
                    gratitude: "Gratitude Practice. Bring to mind three things you're grateful for today. They can be simple: a warm cup, a kind word, a moment of beauty. Feel the warmth of gratitude in your heart. Let it expand with each breath. Gratitude opens the door to more joy. Carry this feeling with you."
                };
                
                const text = scripts[type] || "Take a moment to breathe and relax.";
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 0.9;
                utterance.pitch = 1.1;
                
                // Select a nice voice if available
                try {
                    const voices = await loadVoices();
                    const preferred = voices.find(v => v.lang.includes('en') && v.name.includes('Google') || v.name.includes('Samantha'));
                    if (preferred) utterance.voice = preferred;
                } catch(e) {}
                
                utterance.onend = () => { speechActive = false; };
                utterance.onerror = () => { speechActive = false; };
                
                window.speechSynthesis.speak(utterance);
                speechUtterance = utterance;
            };
            
            // ----- Body Scan with Speech -----
            let bodyScanActive = false;
            let bodyScanInterval;
            let bodyScanParts = [
                "Close your eyes and take a deep breath...",
                "Focus on your head. Release any tension in your forehead.",
                "Relax your jaw and face muscles. Let your expression soften.",
                "Let your shoulders drop and relax.",
                "Feel your arms becoming heavy and relaxed.",
                "Notice your hands. Let them rest comfortably.",
                "Breathe into your chest and stomach. Feel them expand and release.",
                "Relax your lower back and hips.",
                "Feel your legs becoming heavy and sinking into the surface.",
                "Finally, relax your feet and toes.",
                "Take a deep breath. You are completely relaxed.",
                "When ready, slowly open your eyes."
            ];
            
            window.startBodyScan = function() {
                const textEl = document.getElementById('bodyScanText');
                const btn = document.getElementById('bodyScanBtn');
                
                if (bodyScanActive) {
                    bodyScanActive = false;
                    clearInterval(bodyScanInterval);
                    stopSpeech();
                    textEl.textContent = 'Press start to begin the body scan';
                    btn.innerHTML = '<i class="fas fa-play"></i> Start Body Scan';
                    return;
                }
                
                bodyScanActive = true;
                btn.innerHTML = '<i class="fas fa-stop"></i> Stop';
                stopSpeech();
                
                let index = 0;
                
                function speakPart(text) {
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.rate = 0.85;
                    utterance.pitch = 1.0;
                    window.speechSynthesis.speak(utterance);
                }
                
                textEl.textContent = bodyScanParts[index];
                speakPart(bodyScanParts[index]);
                
                bodyScanInterval = setInterval(() => {
                    index++;
                    if (index >= bodyScanParts.length) {
                        bodyScanActive = false;
                        clearInterval(bodyScanInterval);
                        btn.innerHTML = '<i class="fas fa-play"></i> Start Body Scan';
                        textEl.textContent = 'Body scan complete. Well done.';
                        return;
                    }
                    textEl.textContent = bodyScanParts[index];
                    speakPart(bodyScanParts[index]);
                }, 6000);
            };
            
            // ----- Breathing Exercise -----
            let breathingActive = false;
            let breathingInterval;
            
            window.toggleBreathing = function() {
                const circle = document.getElementById('breathingCircle');
                const btn = document.getElementById('breathBtn');
                
                if (breathingActive) {
                    breathingActive = false;
                    clearInterval(breathingInterval);
                    circle.style.transform = 'scale(1)';
                    circle.textContent = 'Press Start';
                    btn.innerHTML = '<i class="fas fa-play"></i> Start Breathing';
                    return;
                }
                
                breathingActive = true;
                btn.innerHTML = '<i class="fas fa-stop"></i> Stop';
                
                const phases = [
                    { text: 'Breathe In', scale: 1.3, duration: 4000 },
                    { text: 'Hold', scale: 1.3, duration: 4000 },
                    { text: 'Breathe Out', scale: 1, duration: 4000 },
                    { text: 'Hold', scale: 1, duration: 4000 }
                ];
                
                let phaseIndex = 0;
                
                function nextPhase() {
                    const phase = phases[phaseIndex];
                    circle.textContent = phase.text;
                    circle.style.transform = `scale(${phase.scale})`;
                    phaseIndex = (phaseIndex + 1) % phases.length;
                }
                
                nextPhase();
                breathingInterval = setInterval(nextPhase, 4000);
            };
            
            // Cleanup on page unload
            window.addEventListener('beforeunload', () => {
                stopAllSounds();
                if (breathingInterval) clearInterval(breathingInterval);
                if (bodyScanInterval) clearInterval(bodyScanInterval);
            });
            
        })();
    </script>
{% endblock %}
'''

RESOURCES_TEMPLATE = '''
{% extends "base" %}
{% block content %}
    <div class="dashboard">
        <div class="welcome-banner">
            <h1>Self-Help Resources 📚</h1>
            <p>Knowledge and tools for your mental wellness journey</p>
        </div>
        
        <div class="features" style="padding: 2rem 0;">
            <div class="resources-grid">
                <!-- Anxiety -->
                <div class="resource-card">
                    <div class="resource-header" style="background: linear-gradient(135deg, #A7C7E7, #87CEEB);">
                        <h3>🌊 Understanding & Managing Anxiety</h3>
                    </div>
                    <div class="resource-content">
                        <p><strong>What is anxiety?</strong> Anxiety is your body's natural response to stress. It's normal to feel anxious sometimes, but when it becomes overwhelming, there are tools that can help.</p>
                        
                        <h4 style="margin: 1rem 0 0.5rem; color: var(--text-dark);">Quick Relief Techniques:</h4>
                        <ul style="color: var(--text-light); line-height: 1.8; padding-left: 1.5rem;">
                            <li><strong>5-4-3-2-1 Grounding:</strong> Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste</li>
                            <li><strong>Box Breathing:</strong> Breathe in for 4 counts, hold for 4, out for 4, hold for 4</li>
                            <li><strong>Cold Water:</strong> Splash cold water on your face to activate the dive reflex</li>
                        </ul>
                    </div>
                </div>
                
                <!-- Depression -->
                <div class="resource-card">
                    <div class="resource-header" style="background: linear-gradient(135deg, #E6E6FA, #DDA0DD);">
                        <h3>💜 Coping with Depression</h3>
                    </div>
                    <div class="resource-content">
                        <p><strong>Depression is not your fault.</strong> It's a real medical condition that affects millions of people. Recovery is possible, and you deserve support.</p>
                        
                        <h4 style="margin: 1rem 0 0.5rem; color: var(--text-dark);">Small Steps That Help:</h4>
                        <ul style="color: var(--text-light); line-height: 1.8; padding-left: 1.5rem;">
                            <li>Get outside for even 5 minutes of sunlight</li>
                            <li>Move your body gently - a short walk counts</li>
                            <li>Reach out to one person today</li>
                            <li>Do one small thing that used to bring joy</li>
                            <li>Practice self-compassion - treat yourself like a friend</li>
                        </ul>
                    </div>
                </div>
                
                <!-- Stress -->
                <div class="resource-card">
                    <div class="resource-header" style="background: linear-gradient(135deg, #C1E1C1, #98D8AA);">
                        <h3>🌿 Managing Stress</h3>
                    </div>
                    <div class="resource-content">
                        <p><strong>Stress is manageable.</strong> While we can't always control our circumstances, we can build resilience and coping strategies.</p>
                        
                        <h4 style="margin: 1rem 0 0.5rem; color: var(--text-dark);">Stress-Busting Strategies:</h4>
                        <ul style="color: var(--text-light); line-height: 1.8; padding-left: 1.5rem;">
                            <li><strong>Time-blocking:</strong> Schedule breaks, not just tasks</li>
                            <li><strong>Boundaries:</strong> It's okay to say no</li>
                            <li><strong>Movement:</strong> Physical activity reduces cortisol</li>
                            <li><strong>Connection:</strong> Talk to someone you trust</li>
                            <li><strong>Sleep:</strong> Prioritize 7-9 hours nightly</li>
                        </ul>
                    </div>
                </div>
                
                <!-- Sleep -->
                <div class="resource-card">
                    <div class="resource-header" style="background: linear-gradient(135deg, #9370DB, #7B68A6);">
                        <h3>🌙 Better Sleep Guide</h3>
                    </div>
                    <div class="resource-content">
                        <p><strong>Sleep is foundational.</strong> Poor sleep affects mood, cognition, and overall mental health. Small changes can make a big difference.</p>
                        
                        <h4 style="margin: 1rem 0 0.5rem; color: var(--text-dark);">Sleep Hygiene Tips:</h4>
                        <ul style="color: var(--text-light); line-height: 1.8; padding-left: 1.5rem;">
                            <li>Keep a consistent sleep schedule</li>
                            <li>Avoid screens 1 hour before bed</li>
                            <li>Keep your room cool and dark</li>
                            <li>Limit caffeine after 2 PM</li>
                            <li>Create a relaxing bedtime routine</li>
                        </ul>
                    </div>
                </div>
                
                <!-- Self-Care -->
                <div class="resource-card">
                    <div class="resource-header" style="background: linear-gradient(135deg, #FFE4E9, #FFB6C1);">
                        <h3>🌸 Self-Care Essentials</h3>
                    </div>
                    <div class="resource-content">
                        <p><strong>Self-care isn't selfish.</strong> Taking care of yourself enables you to show up better for everything else in your life.</p>
                        
                        <h4 style="margin: 1rem 0 0.5rem; color: var(--text-dark);">Self-Care Ideas:</h4>
                        <ul style="color: var(--text-light); line-height: 1.8; padding-left: 1.5rem;">
                            <li>🛁 Take a warm bath or shower</li>
                            <li>📖 Read something enjoyable</li>
                            <li>🎵 Listen to music that lifts you</li>
                            <li>🌳 Spend time in nature</li>
                            <li>☕ Enjoy a warm drink mindfully</li>
                            <li>💬 Connect with a loved one</li>
                        </ul>
                    </div>
                </div>
                
                <!-- Crisis Resources -->
                <div class="resource-card">
                    <div class="resource-header" style="background: linear-gradient(135deg, #E57373, #EF5350);">
                        <h3>🆘 Crisis Support</h3>
                    </div>
                    <div class="resource-content">
                        <p><strong>You matter.</strong> If you're in crisis or having thoughts of self-harm, please reach out. Help is available 24/7.</p>
                        
                        <h4 style="margin: 1rem 0 0.5rem; color: var(--text-dark);">Immediate Help:</h4>
                        <ul style="color: var(--text-light); line-height: 2; padding-left: 1.5rem; list-style: none;">
                            <li>📞 <strong>KIRAN Helpline</strong> - 1800-599-0019</li>
                            <li>💬 <strong>iCall</strong> - 9152987821 (Mon-Sat, 10am-8pm)</li>
                            <li>📞 <strong>Vandrevala Foundation</strong> - 1860-266-2345 (24/7)</li>
                            <li>🌍 <a href="https://www.thelivelovelaughfoundation.org/find-help/helplines" target="_blank">More Indian Helplines</a></li>
                        </ul>
                        
                        <p style="margin-top: 1rem; font-style: italic;">Remember: Reaching out for help is a sign of strength, not weakness.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
{% endblock %}
'''

def render(template, **kwargs):
    """Render a template with the base template."""
    full_template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', template)
    return render_template_string(full_template, **kwargs)

# ROUTES 

@app.route('/')
def home():
    return render(HOME_TEMPLATE.replace('{% extends "base" %}', '').replace('{% block content %}', '').replace('{% endblock %}', ''))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in users_db and check_password_hash(users_db[email]['password'], password):
            session['user'] = email
            session['name'] = users_db[email]['name']
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid email or password. Please try again."
    
    template = LOGIN_TEMPLATE.replace('{% extends "base" %}', '').replace('{% block content %}', '').replace('{% endblock %}', '')
    return render(template, error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if email in users_db:
            error = "This email is already registered. Please sign in instead."
        elif password != confirm_password:
            error = "Passwords don't match. Please try again."
        elif len(password) < 6:
            error = "Password must be at least 6 characters long."
        else:
            users_db[email] = {
                'name': name,
                'password': generate_password_hash(password)
            }
            moods_db[email] = []
            journals_db[email] = []
            session['user'] = email
            session['name'] = name
            return redirect(url_for('dashboard'))
    
    template = REGISTER_TEMPLATE.replace('{% extends "base" %}', '').replace('{% block content %}', '').replace('{% endblock %}', '')
    return render(template, error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user_moods = moods_db.get(session['user'], [])
    user_journals = journals_db.get(session['user'], [])
    
    template = DASHBOARD_TEMPLATE.replace('{% extends "base" %}', '').replace('{% block content %}', '').replace('{% endblock %}', '')
    return render(template, moods=user_moods, journals=user_journals)

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    success = None
    if request.method == 'POST':
        content = request.form.get('content')
        mood = request.form.get('mood')
        
        if content:
            entry = {
                'date': datetime.now().strftime('%B %d, %Y at %I:%M %p'),
                'content': content,
                'mood': mood
            }
            if session['user'] not in journals_db:
                journals_db[session['user']] = []
            journals_db[session['user']].append(entry)
            success = "Your journal entry has been saved 💜"
    
    user_journals = journals_db.get(session['user'], [])
    template = JOURNAL_TEMPLATE.replace('{% extends "base" %}', '').replace('{% block content %}', '').replace('{% endblock %}', '')
    return render(template, journals=user_journals, success=success)

@app.route('/meditation')
def meditation():
    template = MEDITATION_TEMPLATE.replace('{% extends "base" %}', '').replace('{% block content %}', '').replace('{% endblock %}', '')
    return render(template)

@app.route('/resources')
def resources():
    template = RESOURCES_TEMPLATE.replace('{% extends "base" %}', '').replace('{% block content %}', '').replace('{% endblock %}', '')
    return render(template)

@app.route('/api/mood', methods=['POST'])
def save_mood():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    emoji = data.get('emoji')
    mood = data.get('mood')
    
    if session['user'] not in moods_db:
        moods_db[session['user']] = []
    
    moods_db[session['user']].append({
        'emoji': emoji,
        'mood': mood,
        'date': datetime.now().strftime('%b %d')
    })
    
    return jsonify({'success': True})

# RUN APP 

if __name__ == '__main__':
    print("\n" + "="*60)
    print("💜 Qulb - Your Mental Wellness Companion")
    print("="*60)
    print("\n✨ Starting server...")
    print("📍 Open your browser and go to: http://localhost:5000")
    print("\n💜 Features:")
    print("   • User registration & login")
    print("   • Mood tracking")
    print("   • Private journaling")
    print("   • Meditation exercises")
    print("   • Self-help resources")
    print("   • Crisis support (Indian helplines)")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, port=5000)