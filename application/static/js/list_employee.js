

const viewedEmployee = () => {
    fetch("/view_camera")
        .then(res => res.json())
        .then((data) => {
            let results = data.results;
            let view_employee = document.querySelector("#view_employee");
            results.forEach(data => {
                view_employee.innerHTML = `
                
                <tr>
                    <td>${data.name}</td>
                    <td>${data.position}</td>
                    <td>${data.address}</td>
                    <td>${data.contact}</td>
                </tr>
            
            `
            });
            
        })
        .catch(error => {
            console.error('Error:', error);
        });
};


viewedEmployee();
