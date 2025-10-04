<?php
/**
 * Foxcode Shorter - Admin Login
 * Bootstrap dark theme login page
 */

require_once 'config.php';

$error = '';
$success = '';

// Handle login
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = sanitizeInput($_POST['username'] ?? '');
    $password = sanitizeInput($_POST['password'] ?? '');

    if ($username === ADMIN_USERNAME && $password === ADMIN_PASSWORD) {
        $_SESSION['admin_logged_in'] = true;
        $_SESSION['admin_username'] = $username;
        $_SESSION['login_time'] = time();

        header('Location: dashboard.php');
        exit;
    } else {
        $error = 'Invalid username or password!';
    }
}

// Redirect if already logged in
if (isLoggedIn()) {
    header('Location: dashboard.php');
    exit;
}
?>

<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login - <?php echo APP_NAME; ?></title>

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">

    <style>
        body {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f172a 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .login-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .brand-logo {
            font-size: 2.5rem;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 2rem;
        }

        .form-control:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
        }

        .btn-primary {
            background: linear-gradient(45deg, #667eea, #764ba2);
            border: none;
            padding: 12px 30px;
            font-weight: 500;
        }

        .btn-primary:hover {
            background: linear-gradient(45deg, #764ba2, #667eea);
            transform: translateY(-1px);
            transition: all 0.3s ease;
        }

        .alert {
            border-radius: 10px;
            border: none;
        }

        .version-info {
            position: fixed;
            bottom: 20px;
            right: 20px;
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.8rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6 col-lg-4">
                <div class="card login-card">
                    <div class="card-body p-5">
                        <div class="brand-logo">
                            <i class="bi bi-link-45deg"></i>
                            <div><?php echo APP_NAME; ?></div>
                        </div>

                        <h4 class="text-center mb-4 text-light">Admin Panel Login</h4>

                        <?php if ($error): ?>
                            <div class="alert alert-danger">
                                <i class="bi bi-exclamation-triangle me-2"></i>
                                <?php echo $error; ?>
                            </div>
                        <?php endif; ?>

                        <?php if ($success): ?>
                            <div class="alert alert-success">
                                <i class="bi bi-check-circle me-2"></i>
                                <?php echo $success; ?>
                            </div>
                        <?php endif; ?>

                        <form method="POST" action="">
                            <div class="mb-4">
                                <label for="username" class="form-label">
                                    <i class="bi bi-person me-2"></i>Username
                                </label>
                                <input type="text" class="form-control form-control-lg" 
                                       id="username" name="username" required 
                                       placeholder="Enter admin username"
                                       value="<?php echo htmlspecialchars($_POST['username'] ?? ''); ?>">
                            </div>

                            <div class="mb-4">
                                <label for="password" class="form-label">
                                    <i class="bi bi-lock me-2"></i>Password
                                </label>
                                <input type="password" class="form-control form-control-lg" 
                                       id="password" name="password" required 
                                       placeholder="Enter admin password">
                            </div>

                            <div class="d-grid mb-4">
                                <button type="submit" class="btn btn-primary btn-lg">
                                    <i class="bi bi-box-arrow-in-right me-2"></i>
                                    Login to Admin Panel
                                </button>
                            </div>

                            <div class="text-center">
                                <small class="text-muted">
                                    <i class="bi bi-shield-lock me-1"></i>
                                    Secure admin access only
                                </small>
                            </div>
                        </form>
                    </div>
                </div>

                <div class="text-center mt-3">
                    <small class="text-muted">
                        Created by <strong>codewithkanchan.com</strong>
                    </small>
                </div>
            </div>
        </div>
    </div>

    <div class="version-info">
        Version <?php echo APP_VERSION; ?>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

    <script>
        // Auto-focus on username field
        document.getElementById('username').focus();

        // Clear form on page load
        if (performance.navigation.type === 1) {
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';
        }
    </script>
</body>
</html>