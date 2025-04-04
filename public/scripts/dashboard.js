document.addEventListener('DOMContentLoaded', function () {
        const typeRadios = document.querySelectorAll('input[name="insurance_type"]');
        const planOptions = document.getElementById('plan_options');

        typeRadios.forEach(radio => {
            radio.addEventListener('change', function () {
                if (this.value === 'plan') {
                    planOptions.style.display = 'block';
                } else {
                    planOptions.style.display = 'none';
                }
            });
        });
    });

createInsuranceList(fetchInsurances())

async function fetchInsurances()
{
    try
    {
        const response = await fetch('/api/all-my-insurances')
        const data = await response.json()
        if (!response.ok)
        {
            alert(data.error)
        }
        return await response.json()
    }
    catch (error)
    {
        console.error('Error fetching insurances:', error)
        return []
    }
}

function createInsuranceList(insurances)
{
    // Select the dashboard container where the insurance list will be appended
    const dashboardContainer = document.querySelector('.dashboard-container')

    if (!dashboardContainer)
    {
        console.error('Dashboard container not found')
        return
    }

    let insuranceList = document.querySelector('.insurance-list')

    if (!insuranceList)
    {
        insuranceList = document.createElement('div')
        insuranceList.className = 'insurance-list'
        dashboardContainer.appendChild(insuranceList)

        const h2 = document.createElement('h2')
        h2.textContent = 'Existing Insurances'
        h2.style.marginBottom = '15px'
        insuranceList.appendChild(h2)
    }
    else
    {
        const existingItems = insuranceList.querySelectorAll('.insurance-item')
        existingItems.forEach(item => item.remove())
    }

    insurances.forEach(insurance => {
        const itemDiv = document.createElement('div')
        itemDiv.className = 'insurance-item'

        const nameP = document.createElement('p')
        nameP.className = 'insurance-name'
        nameP.textContent = insurance.name

        const uuidP = document.createElement('p')
        uuidP.className = 'insurance-uuid'
        uuidP.textContent = `UUID: ${insurance.uuid}`

        itemDiv.appendChild(nameP)
        itemDiv.appendChild(uuidP)
        insuranceList.appendChild(itemDiv)
    })
}