<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Syed Qasim Ali - Solo Leveling Profile</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
            color: #e0e0e0;
            overflow-x: hidden;
            position: relative;
        }

        /* Animated background particles */
        .particle {
            position: fixed;
            width: 3px;
            height: 3px;
            background: rgba(138, 180, 248, 0.5);
            border-radius: 50%;
            animation: float 15s infinite;
            z-index: 0;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0) translateX(0); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(-100vh) translateX(50px); opacity: 0; }
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }

        /* Header with glow effect */
        .header {
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(135deg, rgba(26, 26, 46, 0.9), rgba(22, 33, 62, 0.9));
            border-radius: 20px;
            margin-bottom: 40px;
            position: relative;
            overflow: hidden;
            border: 2px solid rgba(138, 180, 248, 0.3);
            box-shadow: 0 0 40px rgba(138, 180, 248, 0.2);
            animation: fadeInDown 1s ease-out;
        }

        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(138, 180, 248, 0.1), transparent);
            animation: shine 3s infinite;
        }

        @keyframes shine {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .header h1 {
            font-size: 3.5em;
            font-weight: 900;
            background: linear-gradient(135deg, #8ab4f8 0%, #5e9cff 50%, #4a90ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
            text-shadow: 0 0 30px rgba(138, 180, 248, 0.5);
            animation: glow 2s ease-in-out infinite alternate;
            position: relative;
            z-index: 1;
        }

        @keyframes glow {
            from { filter: drop-shadow(0 0 10px rgba(138, 180, 248, 0.5)); }
            to { filter: drop-shadow(0 0 20px rgba(138, 180, 248, 0.8)); }
        }

        .subtitle {
            font-size: 1.3em;
            color: #8ab4f8;
            margin-top: 10px;
            position: relative;
            z-index: 1;
            animation: fadeIn 1.5s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .rank-badge {
            display: inline-block;
            padding: 12px 30px;
            background: linear-gradient(135deg, #8ab4f8, #5e9cff);
            border-radius: 30px;
            margin-top: 20px;
            font-weight: bold;
            font-size: 1.2em;
            color: #0a0e27;
            box-shadow: 0 5px 20px rgba(138, 180, 248, 0.4);
            animation: pulse 2s ease-in-out infinite;
            position: relative;
            z-index: 1;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
            animation: fadeInUp 1s ease-out 0.3s backwards;
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

        .stat-card {
            background: linear-gradient(135deg, rgba(26, 26, 46, 0.95), rgba(22, 33, 62, 0.95));
            padding: 30px;
            border-radius: 15px;
            border: 2px solid rgba(138, 180, 248, 0.2);
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }

        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(138, 180, 248, 0.1), transparent);
            transition: left 0.5s ease;
        }

        .stat-card:hover::before {
            left: 100%;
        }

        .stat-card:hover {
            transform: translateY(-10px) scale(1.02);
            border-color: rgba(138, 180, 248, 0.6);
            box-shadow: 0 10px 40px rgba(138, 180, 248, 0.3);
        }

        .stat-card h3 {
            color: #8ab4f8;
            font-size: 1.3em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .stat-icon {
            font-size: 1.5em;
            animation: rotate 3s linear infinite;
        }

        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(135deg, #fff, #8ab4f8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        /* Skills Section */
        .skills-section {
            background: linear-gradient(135deg, rgba(26, 26, 46, 0.95), rgba(22, 33, 62, 0.95));
            padding: 40px;
            border-radius: 20px;
            margin-bottom: 40px;
            border: 2px solid rgba(138, 180, 248, 0.3);
            animation: fadeInUp 1s ease-out 0.6s backwards;
        }

        .skills-section h2 {
            font-size: 2.5em;
            color: #8ab4f8;
            margin-bottom: 30px;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 3px;
        }

        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 20px;
        }

        .skill-item {
            background: linear-gradient(135deg, rgba(138, 180, 248, 0.1), rgba(94, 156, 255, 0.1));
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            transition: all 0.4s ease;
            border: 2px solid transparent;
            position: relative;
            overflow: hidden;
        }

        .skill-item::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(138, 180, 248, 0.2);
            transform: translate(-50%, -50%);
            transition: width 0.5s ease, height 0.5s ease;
        }

        .skill-item:hover::after {
            width: 200%;
            height: 200%;
        }

        .skill-item:hover {
            transform: translateY(-10px) scale(1.1);
            border-color: rgba(138, 180, 248, 0.5);
            box-shadow: 0 10px 30px rgba(138, 180, 248, 0.3);
        }

        .skill-icon {
            font-size: 3em;
            margin-bottom: 10px;
            position: relative;
            z-index: 1;
        }

        .skill-name {
            color: #e0e0e0;
            font-weight: bold;
            position: relative;
            z-index: 1;
        }

        /* Contact Section */
        .contact-section {
            background: linear-gradient(135deg, rgba(26, 26, 46, 0.95), rgba(22, 33, 62, 0.95));
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            border: 2px solid rgba(138, 180, 248, 0.3);
            animation: fadeInUp 1s ease-out 0.9s backwards;
        }

        .contact-section h2 {
            font-size: 2.5em;
            color: #8ab4f8;
            margin-bottom: 30px;
            text-transform: uppercase;
            letter-spacing: 3px;
        }

        .contact-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }

        .contact-btn {
            padding: 15px 35px;
            background: linear-gradient(135deg, #8ab4f8, #5e9cff);
            color: #0a0e27;
            text-decoration: none;
            border-radius: 30px;
            font-weight: bold;
            font-size: 1.1em;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(138, 180, 248, 0.3);
            position: relative;
            overflow: hidden;
        }

        .contact-btn::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.5s ease, height 0.5s ease;
        }

        .contact-btn:hover::before {
            width: 300px;
            height: 300px;
        }

        .contact-btn:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 10px 30px rgba(138, 180, 248, 0.5);
        }

        .contact-btn span {
            position: relative;
            z-index: 1;
        }

        /* Level Progress Bar */
        .level-progress {
            background: rgba(26, 26, 46, 0.95);
            padding: 30px;
            border-radius: 15px;
            margin: 40px 0;
            border: 2px solid rgba(138, 180, 248, 0.3);
            animation: fadeInUp 1s ease-out 1.2s backwards;
        }

        .level-info {
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
            color: #8ab4f8;
            font-weight: bold;
            font-size: 1.2em;
        }

        .progress-bar {
            height: 30px;
            background: rgba(138, 180, 248, 0.1);
            border-radius: 15px;
            overflow: hidden;
            position: relative;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #8ab4f8, #5e9cff, #4a90ff);
            border-radius: 15px;
            animation: fillProgress 2s ease-out forwards;
            position: relative;
            overflow: hidden;
        }

        .progress-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            animation: shimmer 2s infinite;
        }

        @keyframes fillProgress {
            from { width: 0; }
            to { width: 78%; }
        }

        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2em;
            }

            .stats-grid {
                grid-template-columns: 1fr;
            }

            .skills-grid {
                grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            }

            .contact-links {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
</head>
<body>
    <!-- Animated particles -->
    <script>
        for (let i = 0; i < 30; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 15 + 's';
            particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
            document.body.appendChild(particle);
        }
    </script>

    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>⚔️ SYED QASIM ALI ⚔️</h1>
            <p class="subtitle">Frontend Developer | Associate Software Developer</p>
            <div class="rank-badge">🌟 S-RANK HUNTER 🌟</div>
        </div>

        <!-- Level Progress -->
        <div class="level-progress">
            <div class="level-info">
                <span>📊 DEVELOPER LEVEL: 78</span>
                <span>EXP: 78,450 / 100,000</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill"></div>
            </div>
        </div>

        <!-- Stats Grid -->
        <div class="stats-grid">
            <div class="stat-card">
                <h3><span class="stat-icon">💻</span> Total Projects</h3>
                <div class="stat-value">50+</div>
            </div>
            <div class="stat-card">
                <h3><span class="stat-icon">🔥</span> Commit Streak</h3>
                <div class="stat-value">365</div>
            </div>
            <div class="stat-card">
                <h3><span class="stat-icon">⭐</span> Stars Earned</h3>
                <div class="stat-value">1.2K</div>
            </div>
            <div class="stat-card">
                <h3><span class="stat-icon">🎯</span> Pull Requests</h3>
                <div class="stat-value">200+</div>
            </div>
        </div>

        <!-- Skills Section -->
        <div class="skills-section">
            <h2>⚡ HUNTER ABILITIES ⚡</h2>
            <div class="skills-grid">
                <div class="skill-item">
                    <div class="skill-icon">⚛️</div>
                    <div class="skill-name">React</div>
                </div>
                <div class="skill-item">
                    <div class="skill-icon">📜</div>
                    <div class="skill-name">JavaScript</div>
                </div>
                <div class="skill-item">
                    <div class="skill-icon">🎨</div>
                    <div class="skill-name">HTML5</div>
                </div>
                <div class="skill-item">
                    <div class="skill-icon">💎</div>
                    <div class="skill-name">CSS3</div>
                </div>
                <div class="skill-item">
                    <div class="skill-icon">🟢</div>
                    <div class="skill-name">Node.js</div>
                </div>
                <div class="skill-item">
                    <div class="skill-icon">🔱</div>
                    <div class="skill-name">Git</div>
                </div>
                <div class="skill-item">
                    <div class="skill-icon">💼</div>
                    <div class="skill-name">VS Code</div>
                </div>
                <div class="skill-item">
                    <div class="skill-icon">🎯</div>
                    <div class="skill-name">TypeScript</div>
                </div>
            </div>
        </div>

        <!-- Contact Section -->
        <div class="contact-section">
            <h2>🌐 CONNECT WITH ME 🌐</h2>
            <div class="contact-links">
                <a href="https://github.com/s-q-ali" target="_blank" class="contact-btn">
                    <span>💻 GitHub</span>
                </a>
                <a href="https://linkedin.com/in/s-qasim-ali" target="_blank" class="contact-btn">
                    <span>💼 LinkedIn</span>
                </a>
                <a href="mailto:syedqasim963@gmail.com" target="_blank" class="contact-btn">
                    <span>📧 Email</span>
                </a>
                <a href="https://www.instagram.com/syedqasim963" target="_blank" class="contact-btn">
                    <span>📱 Instagram</span>
                </a>
            </div>
        </div>
    </div>
</body>
</html>
