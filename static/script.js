    // Load user list from local storage when the page loads
    document.addEventListener('DOMContentLoaded', function () {
        const savedUserList = localStorage.getItem('userList');
        if (savedUserList) {
            document.getElementById('userListInput').value = savedUserList;
        }
    });

    // Function to open the User List modal
    function openUserListModal() {
        document.getElementById('userListModal').style.display = 'block';
    }

    // Function to close the User List modal
    function closeUserListModal() {
        document.getElementById('userListModal').style.display = 'none';
    }

    // Function to submit the User List
    function submitUserList() {
        const userList = document.getElementById('userListInput').value;
        if (userList) {
            fetch('/update_user_list', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_list: userList.split(',').map(user => user.trim()) })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    localStorage.setItem('userList', userList);
                    closeUserListModal();
                    window.location.reload();
                }
            });
        }
    }

    // Close modal
    window.onclick = function(event) {
    const modal = document.getElementById('userListModal');
    if (event.target === modal) {
        closeUserListModal();
    }
};

setInterval(function () {
    window.location.reload();
}, 60000); // Reloads every 60,000 milliseconds (60 seconds)