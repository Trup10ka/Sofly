document.addEventListener('DOMContentLoaded', function ()
{
    const typeRadios = document.querySelectorAll('input[name="insurance_type"]')
    const planOptions = document.getElementById('plan_options')

    typeRadios.forEach(radio =>
    {
        radio.addEventListener('change', function ()
        {
            if (this.value === 'plan')
            {
                planOptions.style.display = 'block'
            }
            else
            {
                planOptions.style.display = 'none'
            }
        })
    })
})

const createInsuranceButton = document.getElementById('create-insurance-button')

createInsuranceButton.addEventListener('click', async function (event)
{
    event.preventDefault()
    const form = document.getElementById('insurance-form')
    const formData = new FormData(form)
    const plan = formData.get('plan').split(' ')[0].toLowerCase()

    if (!validateForm())
    {
        return
    }

    try
    {
        const response = await fetch('/api/create-insurance', {
            method: 'POST',
            body: JSON.stringify(
                {
                    insurance_type: plan
                }
            ),
            headers: {
                'Content-Type': 'application/json'
            }
        })

        const data = await response.json()

        if (!response.ok)
        {
            alert(data.error)
        }
        else
        {
            alert('Insurance created successfully!')
            form.reset()
            createInsuranceList()
        }
    }
    catch (error)
    {
        console.error('Error creating insurance:', error)
    }
})


createInsuranceList()

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
        return await data
    }
    catch (error)
    {
        console.error('Error fetching insurances:', error)
        return []
    }
}

async function createInsuranceList()
{
    const insurances = await fetchInsurances()
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

    if (insurances.error)
    {
        const errorP = document.createElement('p')
        errorP.className = 'insurance-error'
        errorP.textContent = insurances.error
        insuranceList.appendChild(errorP)
        return
    }

    insurances.forEach(insurance =>
    {
        const itemDiv = document.createElement('div')
        itemDiv.className = 'insurance-item'

        const typeH2 = document.createElement('h2')
        typeH2.textContent = insurance.insurance_type || 'Unknown'
        typeH2.style.color = "#422373"

        const uuidP = document.createElement('p')
        uuidP.className = 'insurance-uuid'
        uuidP.textContent = `UUID: ${insurance.insurance_id}`

        itemDiv.appendChild(typeH2)
        itemDiv.appendChild(uuidP)
        insuranceList.appendChild(itemDiv)
    })
}

function validateForm()
{
    const radios = document.getElementsByName('plan')
    let formValid = false

    for (let i = 0; i < radios.length; i++)
    {
        if (radios[i].checked)
        {
            formValid = true
            break
        }
    }

    if (!formValid)
    {
        alert('Please select at least one plan.')
    }

    return formValid
}