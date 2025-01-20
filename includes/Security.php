<?php
class Security {
    private static $instance = null;
    private const TOKEN_LENGTH = 32;
    private const FORM_TOKEN_NAME = 'form_token';
    private const SESSION_TOKEN_NAME = 'session_token';
    private $token;

    private function __construct() {
        if (session_status() === PHP_SESSION_NONE) {
            session_start();
        }
        $this->initializeToken();
    }

    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function initializeToken() {
        if (!isset($_SESSION['csrf_token'])) {
            $_SESSION['csrf_token'] = self::generateToken();
        }
        $this->token = $_SESSION['csrf_token'];
    }

    public static function sanitizeInput($input) {
        if (is_array($input)) {
            return array_map([self::class, 'sanitizeInput'], $input);
        }
        return htmlspecialchars(trim($input), ENT_QUOTES, 'UTF-8');
    }

    public static function validatePath($path, $baseDir) {
        $realPath = realpath($path);
        $realBaseDir = realpath($baseDir);
        
        if ($realPath === false || $realBaseDir === false) {
            return false;
        }
        
        return strpos($realPath, $realBaseDir) === 0;
    }

    public static function generateToken($length = self::TOKEN_LENGTH) {
        if (function_exists('random_bytes')) {
            $token = bin2hex(random_bytes($length / 2));
        } elseif (function_exists('openssl_random_pseudo_bytes')) {
            $token = bin2hex(openssl_random_pseudo_bytes($length / 2));
        } else {
            $token = bin2hex(uniqid(mt_rand(), true));
        }
        return substr($token, 0, $length);
    }

    public static function generateFormToken() {
        $token = self::generateToken();
        $_SESSION[self::FORM_TOKEN_NAME] = $token;
        return $token;
    }

    public static function validateFormToken($token) {
        if (!isset($_SESSION[self::FORM_TOKEN_NAME])) {
            return false;
        }
        
        $valid = hash_equals($_SESSION[self::FORM_TOKEN_NAME], $token);
        unset($_SESSION[self::FORM_TOKEN_NAME]);
        return $valid;
    }

    public static function generateSessionToken() {
        if (!isset($_SESSION[self::SESSION_TOKEN_NAME])) {
            $_SESSION[self::SESSION_TOKEN_NAME] = self::generateToken();
        }
        return $_SESSION[self::SESSION_TOKEN_NAME];
    }

    public static function validateSessionToken($token) {
        if (!isset($_SESSION[self::SESSION_TOKEN_NAME])) {
            return false;
        }
        return hash_equals($_SESSION[self::SESSION_TOKEN_NAME], $token);
    }

    public static function validateCSRFToken($token) {
        return self::validateSessionToken($token);
    }

    public static function generateCSRFToken() {
        return self::generateSessionToken();
    }

    public static function hashPassword($password) {
        return password_hash($password, PASSWORD_DEFAULT);
    }

    public static function verifyPassword($password, $hash) {
        return password_verify($password, $hash);
    }

    public static function isSecureConnection() {
        return (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
            || $_SERVER['SERVER_PORT'] == 443
            || (!empty($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] == 'https')
            || (!empty($_SERVER['HTTP_X_FORWARDED_SSL']) && $_SERVER['HTTP_X_FORWARDED_SSL'] == 'on');
    }

    public static function setSecureHeaders() {
        header('X-Content-Type-Options: nosniff');
        header('X-Frame-Options: SAMEORIGIN');
        header('X-XSS-Protection: 1; mode=block');
        if (self::isSecureConnection()) {
            header('Strict-Transport-Security: max-age=31536000; includeSubDomains');
        }
    }

    public static function validateEmail($email) {
        return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
    }

    public static function validateURL($url) {
        return filter_var($url, FILTER_VALIDATE_URL) !== false;
    }

    public static function validateIP($ip) {
        return filter_var($ip, FILTER_VALIDATE_IP) !== false;
    }

    public static function validateInteger($value) {
        return filter_var($value, FILTER_VALIDATE_INT) !== false;
    }

    public static function validateFloat($value) {
        return filter_var($value, FILTER_VALIDATE_FLOAT) !== false;
    }

    private function __clone() {}
    public function __wakeup() {}
}
