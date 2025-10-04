<?php
/**
 * Foxcode Shorter - Admin Dashboard
 * Main dashboard with statistics and overview
 */

require_once 'config.php';
requireLogin();

$stats = getStats();
$recentUsers = Database::getInstance()->fetchAll("SELECT * FROM users ORDER BY created_at DESC LIMIT 5");
$recentShortlinks = Database::getInstance()->fetchAll("SELECT s.*, u.username FROM shortlinks s JOIN users u ON s.user_id = u.id ORDER BY s.created_at DESC LIMIT 5");
$pendingPayments = Database::getInstance()->fetchAll("SELECT p.*, u.username FROM payments p JOIN users u ON p.user_id = u.id WHERE p.status = 'pending' ORDER BY p.created_at DESC LIMIT 5");

include 'includes/header.php';
?>

<div class="container-fluid px-4">
    <!-- Page Header -->
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-light">Dashboard</h1>
        <div class="d-flex gap-2">
            <button class="btn btn-outline-light btn-sm" onclick="refreshStats()">
                <i class="bi bi-arrow-clockwise me-1"></i>Refresh
            </button>
            <a href="broadcast.php" class="btn btn-primary btn-sm">
                <i class="bi bi-megaphone me-1"></i>Broadcast
            </a>
        </div>
    </div>

    <!-- Statistics Cards -->
    <div class="row mb-4">
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card bg-primary text-white h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <div class="text-xs font-weight-bold text-uppercase mb-1">Total Users</div>
                            <div class="h5 mb-0 font-weight-bold"><?php echo number_format($stats['total_users']); ?></div>
                        </div>
                        <div class="col-auto">
                            <i class="bi bi-people fa-2x text-white-50"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card bg-success text-white h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <div class="text-xs font-weight-bold text-uppercase mb-1">Total Shortlinks</div>
                            <div class="h5 mb-0 font-weight-bold"><?php echo number_format($stats['total_shortlinks']); ?></div>
                        </div>
                        <div class="col-auto">
                            <i class="bi bi-link-45deg fa-2x text-white-50"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card bg-info text-white h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <div class="text-xs font-weight-bold text-uppercase mb-1">Total Clicks</div>
                            <div class="h5 mb-0 font-weight-bold"><?php echo number_format($stats['total_clicks']); ?></div>
                        </div>
                        <div class="col-auto">
                            <i class="bi bi-cursor-fill fa-2x text-white-50"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card bg-warning text-white h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <div>
                            <div class="text-xs font-weight-bold text-uppercase mb-1">Pending Payments</div>
                            <div class="h5 mb-0 font-weight-bold"><?php echo $stats['pending_payments']; ?></div>
                        </div>
                        <div class="col-auto">
                            <i class="bi bi-clock-fill fa-2x text-white-50"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Revenue Card -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card text-white" style="background: linear-gradient(45deg, #667eea, #764ba2);">
                <div class="card-body">
                    <div class="row align-items-center">
                        <div class="col">
                            <h3 class="mb-0">Total Revenue: <?php echo formatCurrency($stats['total_revenue']); ?></h3>
                            <p class="mb-0">From <?php echo number_format($stats['total_shortlinks']); ?> shortened links</p>
                        </div>
                        <div class="col-auto">
                            <i class="bi bi-currency-rupee fa-3x"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <!-- Recent Users -->
        <div class="col-lg-6 mb-4">
            <div class="card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h6 class="m-0 font-weight-bold text-primary">Recent Users</h6>
                    <a href="users.php" class="btn btn-sm btn-primary">View All</a>
                </div>
                <div class="card-body">
                    <?php if (empty($recentUsers)): ?>
                        <div class="text-center text-muted py-3">
                            <i class="bi bi-people fa-2x mb-2"></i>
                            <p>No users found</p>
                        </div>
                    <?php else: ?>
                        <div class="table-responsive">
                            <table class="table table-sm">
                                <thead>
                                    <tr>
                                        <th>Username</th>
                                        <th>Balance</th>
                                        <th>Joined</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <?php foreach ($recentUsers as $user): ?>
                                        <tr>
                                            <td>
                                                <div class="d-flex align-items-center">
                                                    <div class="avatar-sm bg-primary rounded-circle me-2 d-flex align-items-center justify-content-center">
                                                        <i class="bi bi-person text-white"></i>
                                                    </div>
                                                    <?php echo htmlspecialchars($user['username']); ?>
                                                </div>
                                            </td>
                                            <td><?php echo formatCurrency($user['balance']); ?></td>
                                            <td><?php echo timeAgo($user['created_at']); ?></td>
                                            <td>
                                                <span class="badge bg-<?php echo $user['status'] === 'active' ? 'success' : 'danger'; ?>">
                                                    <?php echo ucfirst($user['status']); ?>
                                                </span>
                                            </td>
                                        </tr>
                                    <?php endforeach; ?>
                                </tbody>
                            </table>
                        </div>
                    <?php endif; ?>
                </div>
            </div>
        </div>

        <!-- Recent Shortlinks -->
        <div class="col-lg-6 mb-4">
            <div class="card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h6 class="m-0 font-weight-bold text-primary">Recent Shortlinks</h6>
                    <a href="shortlinks.php" class="btn btn-sm btn-primary">View All</a>
                </div>
                <div class="card-body">
                    <?php if (empty($recentShortlinks)): ?>
                        <div class="text-center text-muted py-3">
                            <i class="bi bi-link-45deg fa-2x mb-2"></i>
                            <p>No shortlinks found</p>
                        </div>
                    <?php else: ?>
                        <div class="table-responsive">
                            <table class="table table-sm">
                                <thead>
                                    <tr>
                                        <th>Short Code</th>
                                        <th>User</th>
                                        <th>Clicks</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <?php foreach ($recentShortlinks as $link): ?>
                                        <tr>
                                            <td>
                                                <code><?php echo htmlspecialchars($link['short_code']); ?></code>
                                            </td>
                                            <td><?php echo htmlspecialchars($link['username']); ?></td>
                                            <td>
                                                <span class="badge bg-info"><?php echo number_format($link['clicks']); ?></span>
                                            </td>
                                            <td>
                                                <span class="badge bg-<?php echo $link['status'] === 'active' ? 'success' : 'secondary'; ?>">
                                                    <?php echo ucfirst($link['status']); ?>
                                                </span>
                                            </td>
                                        </tr>
                                    <?php endforeach; ?>
                                </tbody>
                            </table>
                        </div>
                    <?php endif; ?>
                </div>
            </div>
        </div>
    </div>

    <!-- Pending Payments -->
    <?php if (!empty($pendingPayments)): ?>
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h6 class="m-0 font-weight-bold text-warning">Pending Payments</h6>
                        <a href="payments.php" class="btn btn-sm btn-warning">Manage All</a>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>User</th>
                                        <th>Amount</th>
                                        <th>Submitted</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <?php foreach ($pendingPayments as $payment): ?>
                                        <tr>
                                            <td>#<?php echo $payment['id']; ?></td>
                                            <td><?php echo htmlspecialchars($payment['username']); ?></td>
                                            <td><?php echo formatCurrency($payment['amount']); ?></td>
                                            <td><?php echo timeAgo($payment['created_at']); ?></td>
                                            <td>
                                                <div class="btn-group btn-group-sm">
                                                    <a href="payments.php?view=<?php echo $payment['id']; ?>" 
                                                       class="btn btn-outline-primary">View</a>
                                                    <button class="btn btn-outline-success" 
                                                            onclick="approvePayment(<?php echo $payment['id']; ?>)">Approve</button>
                                                    <button class="btn btn-outline-danger" 
                                                            onclick="rejectPayment(<?php echo $payment['id']; ?>)">Reject</button>
                                                </div>
                                            </td>
                                        </tr>
                                    <?php endforeach; ?>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    <?php endif; ?>
</div>

<script>
function refreshStats() {
    location.reload();
}

function approvePayment(paymentId) {
    if (confirm('Are you sure you want to approve this payment?')) {
        fetch('ajax/approve_payment.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                payment_id: paymentId,
                action: 'approve'
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error: ' + data.message);
            }
        });
    }
}

function rejectPayment(paymentId) {
    const reason = prompt('Please provide a reason for rejection:');
    if (reason && confirm('Are you sure you want to reject this payment?')) {
        fetch('ajax/approve_payment.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                payment_id: paymentId,
                action: 'reject',
                reason: reason
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error: ' + data.message);
            }
        });
    }
}
</script>

<?php include 'includes/footer.php'; ?>