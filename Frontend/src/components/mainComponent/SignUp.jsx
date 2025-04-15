import React, { useState } from 'react';
import './SignUp.css';
import { useNavigate } from 'react-router-dom';

const SignUp = () => {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState('signup'); // For mobile view toggle between signup/login

    // Sign up logic
    const handleSignUp = async () => {
        const username = document.querySelector("#signup-username").value.trim();
        const email = document.querySelector("#signup-email").value.trim();
        const password = document.querySelector("#signup-password").value.trim();

        // Regular expression to check valid email format
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!username || !email || !password) {
            alert("All fields are required!");
            return;
        }

        if (username.length < 3) {
            alert("Username must be at least 3 characters long!");
            return;
        }

        if (!emailPattern.test(email)) {
            alert("Invalid email format! Please enter a valid email.");
            return;
        }

        if (password.length < 6) {
            alert("Password must be at least 6 characters long!");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/register/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                alert("User created successfully!");
                navigate("/game");
            } else {
                alert(data.error);
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Something went wrong with sign-up!");
        }
    };

    // Login logic
    const handleLogin = async () => {
        const email = document.querySelector("#login-email").value.trim();
        const password = document.querySelector("#login-password").value.trim();

        if (!email || !password) {
            alert("Email and password are required!");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/login/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();
            if (response.ok) {
                alert("Login successful!");
                navigate("/game");
            } else {
                alert("Invalid email or password. Please try again.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Something went wrong with login!");
        }
    };

    // Guest logic
    const handleGuest = () => {
        navigate('/game');  // Guest user directly goes to the game page
    };

    // Toggle between signup and login tabs on mobile
    const toggleTab = (tab) => {
        setActiveTab(tab);
    };

    return (
        <div className="signup">
            <div className="header">
                <h1>Get Started!</h1>
            </div>

            {/* Mobile Tab Switcher */}
            <div className="mobile-tabs">
                <button
                    className={`tab-btn ${activeTab === 'signup' ? 'active' : ''}`}
                    onClick={() => toggleTab('signup')}
                >
                    Sign Up
                </button>
                <button
                    className={`tab-btn ${activeTab === 'login' ? 'active' : ''}`}
                    onClick={() => toggleTab('login')}
                >
                    Login
                </button>
            </div>

            <div className="container">
                {/* Sign Up Box - Only visible on desktop or when signup tab is active */}
                <div className={`box ${activeTab === 'signup' ? 'active-tab' : 'hidden-mobile'}`}>
                    <div className="form">
                        <label className="label">Username</label>
                        <input
                            type="text"
                            id="signup-username"
                            className="input"
                            placeholder="Enter your username"
                        />

                        <label className="label">Email</label>
                        <input
                            type="email"
                            id="signup-email"
                            className="input"
                            placeholder="Enter your email"
                        />

                        <label className="label">Password</label>
                        <input
                            type="password"
                            id="signup-password"
                            className="input"
                            placeholder="Enter your password"
                        />

                        <button className="signupbtn" onClick={handleSignUp}>
                            Sign Up
                        </button>
                    </div>

                    <span className="guest">
                        Don't have an account? Continue as Guest
                    </span>
                    <button onClick={handleGuest} className="guestbtn">
                        Guest Login
                    </button>
                </div>

                {/* Login Box - Only visible on desktop or when login tab is active */}
                <div className={`box ${activeTab === 'login' ? 'active-tab' : 'hidden-mobile'}`}>
                    <div className="form">
                        <label className="label">Email</label>
                        <input
                            type="email"
                            id="login-email"
                            className="input"
                            placeholder="Enter your email"
                        />

                        <label className="label">Password</label>
                        <input
                            type="password"
                            id="login-password"
                            className="input"
                            placeholder="Enter your password"
                        />

                        <button className="LogInbtn" onClick={handleLogin}>
                            LogIn
                        </button>
                    </div>
                </div>
            </div>

            {/* Only show this on mobile */}
            <div className="mobile-guest-section">
                <span className="guest">
                    Don't want to create an account?
                </span>
                <button onClick={handleGuest} className="guestbtn">
                    Continue as Guest
                </button>
            </div>
        </div>
    );
};

export default SignUp;