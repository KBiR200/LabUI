document.getElementById('generateReportBtn').addEventListener('click', function() {
    const selectedMachines = Array.from(document.getElementById('machineSelect').selectedOptions).map(option => option.value);
    const reportSection = document.getElementById('reportSection');
    reportSection.innerHTML = ''; // Clear existing reports

    if (selectedMachines.length > 0) {
        selectedMachines.forEach(machine => {
            const reportCard = document.createElement('div');
            reportCard.classList.add('report-card');

            let formContent = '';

            switch(machine) {
                case 'Machine 1':
                    formContent = `
                        <h3>${machine}</h3>
                        <form>
                            <label for="status-${machine}">Status:</label>
                            <input type="text" id="status-${machine}" name="status-${machine}" placeholder="e.g., Operational">

                            <label for="temperature-${machine}">Temperature:</label>
                            <input type="number" id="temperature-${machine}" name="temperature-${machine}" placeholder="e.g., 75°C">

                            <button type="submit">Submit Report</button>
                        </form>
                    `;
                    break;
                case 'Machine 2':
                    formContent = `
                        <h3>${machine}</h3>
                        <form>
                            <label for="load-${machine}">Load Capacity:</label>
                            <input type="number" id="load-${machine}" name="load-${machine}" placeholder="e.g., 500kg">

                            <label for="hours-${machine}">Operating Hours:</label>
                            <input type="number" id="hours-${machine}" name="hours-${machine}" placeholder="e.g., 1200 hours">

                            <label for="maintenance-${machine}">Maintenance Notes:</label>
                            <textarea id="maintenance-${machine}" name="maintenance-${machine}" rows="3" placeholder="e.g., Scheduled for next week"></textarea>

                            <button type="submit">Submit Report</button>
                        </form>
                    `;
                    break;
                case 'Machine 3':
                    formContent = `
                        <h3>${machine}</h3>
                        <form>
                            <label for="speed-${machine}">Speed:</label>
                            <input type="number" id="speed-${machine}" name="speed-${machine}" placeholder="e.g., 1500 RPM">

                            <label for="voltage-${machine}">Voltage:</label>
                            <input type="number" id="voltage-${machine}" name="voltage-${machine}" placeholder="e.g., 220V">

                            <label for="notes-${machine}">Performance Notes:</label>
                            <textarea id="notes-${machine}" name="notes-${machine}" rows="3" placeholder="e.g., No issues detected"></textarea>

                            <button type="submit">Submit Report</button>
                        </form>
                    `;
                    break;
                case 'Machine 4':
                    formContent = `
                        <h3>${machine}</h3>
                        <form>
                            <label for="pressure-${machine}">Pressure Level:</label>
                            <input type="number" id="pressure-${machine}" name="pressure-${machine}" placeholder="e.g., 5 bar">

                            <label for="flowrate-${machine}">Flow Rate:</label>
                            <input type="number" id="flowrate-${machine}" name="flowrate-${machine}" placeholder="e.g., 300 L/min">

                            <label for="comments-${machine}">Comments:</label>
                            <textarea id="comments-${machine}" name="comments-${machine}" rows="3" placeholder="e.g., Slight vibration observed"></textarea>

                            <button type="submit">Submit Report</button>
                        </form>
                    `;
                    break;
                default:
                    formContent = `
                        <h3>${machine}</h3>
                        <form>
                            <label for="status-${machine}">Status:</label>
                            <input type="text" id="status-${machine}" name="status-${machine}" placeholder="e.g., Operational">

                            <button type="submit">Submit Report</button>
                        </form>
                    `;
            }

            reportCard.innerHTML = formContent;
            reportSection.appendChild(reportCard);
        });
    } else {
        reportSection.innerHTML = '<p id="placeholder">Select machines to generate reports</p>';
    }
});
