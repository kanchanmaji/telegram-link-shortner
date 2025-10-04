<?php
/**
 * Foxcode Shorter - Admin Panel Configuration
 * Database and API configuration for admin panel
 * Created by: codewithkanchan.com
 */

// Start session
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Database Configuration
define('DB_HOST', 'localhost');
define('DB_NAME', 'foxcode_shorter');
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_CHARSET', 'utf8mb4');

// API Configuration
define('API_BASE_URL', 'http://localhost:8000');
define('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE');
define('WEBHOOK_URL', 'https://your-domain.com/webhook.php');

// Admin Configuration
define('ADMIN_USERNAME', 'admin');
define('ADMIN_PASSWORD', 'foxcode123'); // Change this!
define('SESSION_TIMEOUT', 3600); // 1 hour

// Application Configuration
define('APP_NAME', 'Foxcode Shorter');
define('APP_VERSION', '1.0.0');
define('CUSTOM_DOMAIN', 'https://foxcode.tk');
define('SHORTLINK_COST', 10);

// Payment Configuration
define('RAZORPAY_KEY_ID', 'rzp_test_xxxxx');
define('RAZORPAY_KEY_SECRET', 'xxxxx');
define('UPI_ID', 'foxcode@paytm');

// File Upload Configuration
define('UPLOAD_PATH', 'uploads/');
define('MAX_FILE_SIZE', 5 * 1024 * 1024); // 5MB

// Pagination
define('RECORDS_PER_PAGE', 20);

// Database Connection
class Database {
    private static $instance = null;
    private $connection;

    private function __construct() {
        try {
            $dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=" . DB_CHARSET;
            $this->connection = new PDO($dsn, DB_USER, DB_PASS);
            $this->connection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $this->connection->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
        } catch (PDOException $e) {
            die("Database connection failed: " . $e->getMessage());
        }
    }

    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new Database();
        }
        return self::$instance;
    }

    public function getConnection() {
        return $this->connection;
    }

    public function query($sql, $params = []) {
        try {
            $stmt = $this->connection->prepare($sql);
            $stmt->execute($params);
            return $stmt;
        } catch (PDOException $e) {
            throw new Exception("Database query error: " . $e->getMessage());
        }
    }

    public function fetchAll($sql, $params = []) {
        $stmt = $this->query($sql, $params);
        return $stmt->fetchAll();
    }

    public function fetchOne($sql, $params = []) {
        $stmt = $this->query($sql, $params);
        return $stmt->fetch();
    }

    public function lastInsertId() {
        return $this->connection->lastInsertId();
    }
}

// Utility Functions
function isLoggedIn() {
    return isset($_SESSION['admin_logged_in']) && $_SESSION['admin_logged_in'] === true;
}

function requireLogin() {
    if (!isLoggedIn()) {
        header('Location: login.php');
        exit;
    }
}

function formatCurrency($amount) {
    return '₹' . number_format($amount, 2);
}

function formatDate($date) {
    return date('M d, Y H:i', strtotime($date));
}

function timeAgo($datetime) {
    $time = time() - strtotime($datetime);
    $units = array(
        31536000 => 'year',
        2592000 => 'month',
        604800 => 'week',
        86400 => 'day',
        3600 => 'hour',
        60 => 'minute',
        1 => 'second'
    );

    foreach ($units as $unit => $val) {
        if ($time < $unit) continue;
        $numberOfUnits = floor($time / $unit);
        return ($val == 'second') ? 'just now' : 
               $numberOfUnits . ' ' . $val . (($numberOfUnits > 1) ? 's' : '') . ' ago';
    }
}

function sanitizeInput($input) {
    return htmlspecialchars(trim($input), ENT_QUOTES, 'UTF-8');
}

function generateCSRFToken() {
    if (!isset($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

function verifCSRFToken($token) {
    return isset($_SESSION['csrf_token']) && hash_equals($_SESSION['csrf_token'], $token);
}

function sendTelegramMessage($chat_id, $message) {
    $url = "https://api.telegram.org/bot" . BOT_TOKEN . "/sendMessage";
    $data = [
        'chat_id' => $chat_id,
        'text' => $message,
        'parse_mode' => 'Markdown'
    ];

    $options = [
        'http' => [
            'header' => "Content-type: application/x-www-form-urlencoded\r\n",
            'method' => 'POST',
            'content' => http_build_query($data)
        ]
    ];

    $context = stream_context_create($options);
    return file_get_contents($url, false, $context);
}

function callAPI($endpoint, $method = 'GET', $data = null) {
    $url = API_BASE_URL . $endpoint;

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);

    if ($method === 'POST') {
        curl_setopt($ch, CURLOPT_POST, true);
        if ($data) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        }
    } elseif ($method === 'PUT') {
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'PUT');
        if ($data) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        }
    } elseif ($method === 'DELETE') {
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'DELETE');
    }

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    return [
        'status' => $httpCode,
        'data' => json_decode($response, true)
    ];
}

function getStats() {
    $db = Database::getInstance();

    // Get total users
    $totalUsers = $db->fetchOne("SELECT COUNT(*) as count FROM users")['count'] ?? 0;

    // Get total shortlinks
    $totalShortlinks = $db->fetchOne("SELECT COUNT(*) as count FROM shortlinks")['count'] ?? 0;

    // Get total clicks
    $totalClicks = $db->fetchOne("SELECT SUM(clicks) as total FROM shortlinks")['total'] ?? 0;

    // Get pending payments
    $pendingPayments = $db->fetchOne("SELECT COUNT(*) as count FROM payments WHERE status = 'pending'")['count'] ?? 0;

    // Get total revenue
    $totalRevenue = $totalShortlinks * SHORTLINK_COST;

    return [
        'total_users' => $totalUsers,
        'total_shortlinks' => $totalShortlinks,
        'total_clicks' => $totalClicks,
        'pending_payments' => $pendingPayments,
        'total_revenue' => $totalRevenue
    ];
}

// Set default timezone
date_default_timezone_set('Asia/Kolkata');

// Check if tables exist and create them if not
function initializeTables() {
    $db = Database::getInstance();

    // Check if users table exists
    try {
        $db->query("SELECT 1 FROM users LIMIT 1");
    } catch (Exception $e) {
        // Create tables if they don't exist
        $sql = file_get_contents('../database.sql');
        $db->getConnection()->exec($sql);
    }
}

// Initialize tables on first run
// initializeTables();
?>
