document.addEventListener('DOMContentLoaded', function() {
    // Sample data - Replace this with actual data from your backend
    const sampleData = [
        {
            timestamp: '2024-01-20 14:30:25',
            username: 'user123',
            password: '********',
            ip: '192.168.1.1',
            userAgent: 'Mozilla/5.0 (Windows NT 10.0)',
            location: 'New York, US'
        }
        // Add more sample data as needed
    ];

    // Update stats
    document.getElementById('totalAttempts').textContent = sampleData.length;
    document.getElementById('uniqueIPs').textContent = new Set(sampleData.map(d => d.ip)).size;
    document.getElementById('todayAttempts').textContent = sampleData.filter(d => 
        new Date(d.timestamp).toDateString() === new Date().toDateString()
    ).length;

    // Populate table
    const tableBody = document.getElementById('dataTable');
    sampleData.forEach(data => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${data.timestamp}</td>
            <td>${data.username}</td>
            <td>${data.password}</td>
            <td>${data.ip}</td>
            <td>${data.userAgent}</td>
            <td>${data.location}</td>
        `;
        tableBody.appendChild(row);
    });

    // Search functionality
    document.getElementById('searchInput').addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const rows = tableBody.getElementsByTagName('tr');
        
        Array.from(rows).forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });

    // Export functionality
    document.querySelector('.export-btn').addEventListener('click', function() {
        // Implement export logic here
        alert('Export functionality to be implemented');
    });
}); 