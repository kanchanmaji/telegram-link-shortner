<?php
/**
 * Foxcode Shorter - User Management
 * Manage users, balances, and user actions
 */

require_once 'config.php';
requireLogin();

$db = Database::getInstance();
$page = isset($_GET['page']) ? max(1, intval($_GET['page'])) : 1;
$search = isset($_GET['search']) ? sanitizeInput($_GET['search']) : '';
$status_filter = isset($_GET['status']) ? sanitizeInput($_GET['status']) : '';

$offset = ($page - 1) * RECORDS_PER_PAGE;

// Build query conditions
$where_conditions = [];
$params = [];

if ($search) {
    $where_conditions[] = "(username LIKE ? OR telegram_id LIKE ?)";
    $params[] = "%$search%";
    $params[] = "%$search%";
}

if ($status_filter) {
    $where_conditions[] = "status = ?";
    $params[] = $status_filter;
}

$where_clause = !empty($where_conditions) ? 'WHERE ' . implode(' AND ', $where_conditions) : '';

// Get total count
$count_sql = "SELECT COUNT(*) as total FROM users $where_clause";
$total_records = $db->fetchOne($count_sql, $params)['total'];
$total_pages = ceil($total_records / RECORDS_PER_PAGE);

// Get users
$sql = "SELECT u.*, 
               (SELECT COUNT(*) FROM shortlinks WHERE user_id = u.id) as total_links,
               (SELECT COUNT(*) FROM payments WHERE user_id = u.id AND status = 'approved') as total_payments
        FROM users u 
        $where_clause 
        ORDER BY u.created_at DESC 
        LIMIT " . RECORDS_PER_PAGE . " OFFSET $offset";

$users = $db->fetchAll($sql, $params);

// Handle AJAX requests
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    header('Content-Type: application/json');

    $user_id = intval($_POST['user_id'] ?? 0);
    $action = sanitizeInput($_POST['action']);

    switch ($action) {
        case 'update_balance':
            $amount = floatval($_POST['amount'] ?? 0);
            $operation = sanitizeInput($_POST['operation'] ?? 'add');

            $user = $db->fetchOne("SELECT * FROM users WHERE id = ?", [$user_id]);
            if ($user) {
                $new_balance = $operation === 'add' ? 
                    $user['balance'] + $amount : 
                    max(0, $user['balance'] - $amount);

                $db->query("UPDATE users SET balance = ? WHERE id = ?", [$new_balance, $user_id]);

                echo json_encode(['success' => true, 'new_balance' => $new_balance]);
            } else {
                echo json_encode(['success' => false, 'message' => 'User not found']);
            }
            break;

        case 'update_status':
            $new_status = sanitizeInput($_POST['status'] ?? 'active');
            $db->query("UPDATE users SET status = ? WHERE id = ?", [$new_status, $user_id]);
            echo json_encode(['success' => true]);
            break;

        case 'delete_user':
            // Delete user and related data
            $db->query("DELETE FROM payments WHERE user_id = ?", [$user_id]);
            $db->query("DELETE FROM shortlinks WHERE user_id = ?", [$user_id]);
            $db->query("DELETE FROM users WHERE id = ?", [$user_id]);
            echo json_encode(['success' => true]);
            break;
    }
    exit;
}

include 'includes/header.php';
?>

<div class="container-fluid px-4">
    <!-- Page Header -->
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-light">User Management</h1>
        <div class="d-flex gap-2">
            <button class="btn btn-outline-light btn-sm" onclick="exportUsers()">
                <i class="bi bi-download me-1"></i>Export
            </button>
        </div>
    </div>

    <!-- Filters -->
    <div class="card mb-4">
        <div class="card-body">
            <form method="GET" class="row g-3">
                <div class="col-md-4">
                    <label for="search" class="form-label">Search Users</label>
                    <input type="text" class="form-control" id="search" name="search" 
                           placeholder="Username or Telegram ID" value="<?php echo htmlspecialchars($search); ?>">
                </div>
                <div class="col-md-3">
                    <label for="status" class="form-label">Status Filter</label>
                    <select class="form-select" id="status" name="status">
                        <option value="">All Status</option>
                        <option value="active" <?php echo $status_filter === 'active' ? 'selected' : ''; ?>>Active</option>
                        <option value="blocked" <?php echo $status_filter === 'blocked' ? 'selected' : ''; ?>>Blocked</option>
                        <option value="banned" <?php echo $status_filter === 'banned' ? 'selected' : ''; ?>>Banned</option>
                    </select>
                </div>
                <div class="col-md-2">
                    <label class="form-label">&nbsp;</label>
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary">
                            <i class="bi bi-search me-1"></i>Filter
                        </button>
                    </div>
                </div>
                <div class="col-md-2">
                    <label class="form-label">&nbsp;</label>
                    <div class="d-grid">
                        <a href="users.php" class="btn btn-outline-secondary">
                            <i class="bi bi-arrow-clockwise me-1"></i>Reset
                        </a>
                    </div>
                </div>
            </form>
        </div>
    </div>

    <!-- Statistics Cards -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card text-white bg-primary">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <div class="text-xs">Total Users</div>
                            <div class="h5"><?php echo number_format($total_records); ?></div>
                        </div>
                        <i class="bi bi-people fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-white bg-success">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <div class="text-xs">Active Users</div>
                            <div class="h5"><?php echo $db->fetchOne("SELECT COUNT(*) as count FROM users WHERE status = 'active'")['count']; ?></div>
                        </div>
                        <i class="bi bi-person-check fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-white bg-warning">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <div class="text-xs">Blocked Users</div>
                            <div class="h5"><?php echo $db->fetchOne("SELECT COUNT(*) as count FROM users WHERE status = 'blocked'")['count']; ?></div>
                        </div>
                        <i class="bi bi-person-x fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-white bg-info">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <div class="text-xs">Total Balance</div>
                            <div class="h5"><?php echo formatCurrency($db->fetchOne("SELECT SUM(balance) as total FROM users")['total'] ?? 0); ?></div>
                        </div>
                        <i class="bi bi-wallet2 fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Users Table -->
    <div class="card">
        <div class="card-header">
            <h6 class="m-0 font-weight-bold text-primary">Users List</h6>
        </div>
        <div class="card-body">
            <?php if (empty($users)): ?>
                <div class="text-center py-4">
                    <i class="bi bi-people fa-3x text-muted mb-3"></i>
                    <h5 class="text-muted">No Users Found</h5>
                    <p class="text-muted">No users match your current filters.</p>
                </div>
            <?php else: ?>
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>User Info</th>
                                <th>Balance</th>
                                <th>Activity</th>
                                <th>Status</th>
                                <th>Joined</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($users as $user): ?>
                                <tr id="user-<?php echo $user['id']; ?>">
                                    <td>
                                        <div class="d-flex align-items-center">
                                            <div class="avatar bg-primary rounded-circle me-3 d-flex align-items-center justify-content-center" 
                                                 style="width: 40px; height: 40px;">
                                                <i class="bi bi-person text-white"></i>
                                            </div>
                                            <div>
                                                <div class="font-weight-bold"><?php echo htmlspecialchars($user['username']); ?></div>
                                                <small class="text-muted">ID: <?php echo $user['telegram_id']; ?></small>
                                            </div>
                                        </div>
                                    </td>
                                    <td>
                                        <div class="balance-display" id="balance-<?php echo $user['id']; ?>">
                                            <span class="font-weight-bold text-success"><?php echo formatCurrency($user['balance']); ?></span>
                                            <br>
                                            <small class="text-muted"><?php echo floor($user['balance'] / 10); ?> links</small>
                                        </div>
                                    </td>
                                    <td>
                                        <div>
                                            <span class="badge bg-primary"><?php echo $user['total_links']; ?> links</span>
                                            <span class="badge bg-success"><?php echo $user['total_payments']; ?> payments</span>
                                        </div>
                                    </td>
                                    <td>
                                        <select class="form-select form-select-sm" 
                                                onchange="updateUserStatus(<?php echo $user['id']; ?>, this.value)">
                                            <option value="active" <?php echo $user['status'] === 'active' ? 'selected' : ''; ?>>Active</option>
                                            <option value="blocked" <?php echo $user['status'] === 'blocked' ? 'selected' : ''; ?>>Blocked</option>
                                            <option value="banned" <?php echo $user['status'] === 'banned' ? 'selected' : ''; ?>>Banned</option>
                                        </select>
                                    </td>
                                    <td>
                                        <div title="<?php echo formatDate($user['created_at']); ?>">
                                            <?php echo timeAgo($user['created_at']); ?>
                                        </div>
                                    </td>
                                    <td>
                                        <div class="btn-group btn-group-sm">
                                            <button class="btn btn-outline-primary" 
                                                    onclick="editBalance(<?php echo $user['id']; ?>, <?php echo $user['balance']; ?>)">
                                                <i class="bi bi-wallet2"></i>
                                            </button>
                                            <button class="btn btn-outline-info" 
                                                    onclick="viewUserDetails(<?php echo $user['id']; ?>)">
                                                <i class="bi bi-eye"></i>
                                            </button>
                                            <button class="btn btn-outline-danger" 
                                                    onclick="deleteUser(<?php echo $user['id']; ?>, '<?php echo htmlspecialchars($user['username']); ?>')">
                                                <i class="bi bi-trash"></i>
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>

                <!-- Pagination -->
                <?php if ($total_pages > 1): ?>
                    <nav aria-label="Users pagination">
                        <ul class="pagination justify-content-center">
                            <?php if ($page > 1): ?>
                                <li class="page-item">
                                    <a class="page-link" href="?page=<?php echo $page - 1; ?>&search=<?php echo urlencode($search); ?>&status=<?php echo urlencode($status_filter); ?>">
                                        <i class="bi bi-chevron-left"></i>
                                    </a>
                                </li>
                            <?php endif; ?>

                            <?php
                            $start = max(1, $page - 2);
                            $end = min($total_pages, $page + 2);

                            for ($i = $start; $i <= $end; $i++):
                            ?>
                                <li class="page-item <?php echo $i === $page ? 'active' : ''; ?>">
                                    <a class="page-link" href="?page=<?php echo $i; ?>&search=<?php echo urlencode($search); ?>&status=<?php echo urlencode($status_filter); ?>">
                                        <?php echo $i; ?>
                                    </a>
                                </li>
                            <?php endfor; ?>

                            <?php if ($page < $total_pages): ?>
                                <li class="page-item">
                                    <a class="page-link" href="?page=<?php echo $page + 1; ?>&search=<?php echo urlencode($search); ?>&status=<?php echo urlencode($status_filter); ?>">
                                        <i class="bi bi-chevron-right"></i>
                                    </a>
                                </li>
                            <?php endif; ?>
                        </ul>
                    </nav>
                <?php endif; ?>
            <?php endif; ?>
        </div>
    </div>
</div>

<!-- Balance Edit Modal -->
<div class="modal fade" id="balanceModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Edit User Balance</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div class="mb-3">
                    <label for="currentBalance" class="form-label">Current Balance</label>
                    <input type="text" class="form-control" id="currentBalance" readonly>
                </div>
                <div class="mb-3">
                    <label for="operation" class="form-label">Operation</label>
                    <select class="form-select" id="operation">
                        <option value="add">Add Balance</option>
                        <option value="deduct">Deduct Balance</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="amount" class="form-label">Amount (₹)</label>
                    <input type="number" class="form-control" id="amount" min="0" step="0.01" required>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-primary" onclick="saveBalance()">Update Balance</button>
            </div>
        </div>
    </div>
</div>

<script>
let currentUserId = null;

function editBalance(userId, currentBalance) {
    currentUserId = userId;
    document.getElementById('currentBalance').value = '₹' + parseFloat(currentBalance).toFixed(2);
    document.getElementById('amount').value = '';

    const modal = new bootstrap.Modal(document.getElementById('balanceModal'));
    modal.show();
}

function saveBalance() {
    const amount = parseFloat(document.getElementById('amount').value);
    const operation = document.getElementById('operation').value;

    if (!amount || amount <= 0) {
        alert('Please enter a valid amount');
        return;
    }

    const formData = new FormData();
    formData.append('action', 'update_balance');
    formData.append('user_id', currentUserId);
    formData.append('amount', amount);
    formData.append('operation', operation);

    fetch('', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('balance-' + currentUserId).innerHTML = 
                '<span class="font-weight-bold text-success">₹' + parseFloat(data.new_balance).toFixed(2) + '</span><br>' +
                '<small class="text-muted">' + Math.floor(data.new_balance / 10) + ' links</small>';

            bootstrap.Modal.getInstance(document.getElementById('balanceModal')).hide();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating balance');
    });
}

function updateUserStatus(userId, status) {
    const formData = new FormData();
    formData.append('action', 'update_status');
    formData.append('user_id', userId);
    formData.append('status', status);

    fetch('', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Visual feedback
            const row = document.getElementById('user-' + userId);
            row.style.backgroundColor = status === 'active' ? '#d4edda' : 
                                      status === 'blocked' ? '#f8d7da' : '#fff3cd';
            setTimeout(() => {
                row.style.backgroundColor = '';
            }, 2000);
        } else {
            alert('Error updating user status');
        }
    });
}

function deleteUser(userId, username) {
    if (confirm(`Are you sure you want to delete user "${username}"? This will also delete all their links and payments.`)) {
        const formData = new FormData();
        formData.append('action', 'delete_user');
        formData.append('user_id', userId);

        fetch('', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('user-' + userId).remove();
            } else {
                alert('Error deleting user');
            }
        });
    }
}

function viewUserDetails(userId) {
    window.open('user_details.php?id=' + userId, '_blank');
}

function exportUsers() {
    window.location.href = 'export.php?type=users';
}
</script>

<?php include 'includes/footer.php'; ?>