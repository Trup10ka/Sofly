/*
 * #############################################################################
 * This script file was partly generated by Grok AI, ChatGPT and then modified by the developer.
 * https://grok.com/chat/46ba03db-75b4-4aa9-a76f-94a571ce3ba4?referrer=website
 * https://chatgpt.com/share/67f14f8c-10b0-8002-80f4-f2efb826608e
 * ##############################################################################
 * */


document.addEventListener('DOMContentLoaded', () =>
{
    const container = document.getElementById('furniture-container')
    const addButton = document.getElementById('add-furniture')
    let index = 1

    addButton.addEventListener('click', () =>
    {
        const newFieldset = container.firstElementChild.cloneNode(true)

        newFieldset.querySelectorAll('[id]').forEach(el =>
        {
            el.id = el.id.replace('-0', `-${index}`)
        })
        newFieldset.querySelectorAll('label').forEach(label =>
        {
            if (label.htmlFor)
            {
                label.htmlFor = label.htmlFor.replace('-0', `-${index}`)
            }
        })

        newFieldset.querySelectorAll('input').forEach(input =>
        {
            input.value = ''
        })
        newFieldset.querySelectorAll('select').forEach(select =>
        {
            select.selectedIndex = 0
        })

        container.appendChild(newFieldset)
        index++
    })

    container.addEventListener('click', (e) =>
    {
        if (e.target.classList.contains('remove-furniture'))
        {
            const fieldsets = container.querySelectorAll('fieldset')
            if (fieldsets.length > 1)
            {
                e.target.closest('fieldset').remove()
            }
        }
    })
})

async function fetchInsurances()
{
    try
    {
        const response = await fetch('/api/all-my-insurances')
        const insurances = await response.json()

        const select = document.getElementById('insurance')

        if (!Array.isArray(insurances))
        {
            console.error('Invalid response format:', insurances)
            return
        }

        insurances.forEach(insurance =>
        {
            const option = document.createElement('option')
            option.value = insurance.insurance_type
            option.textContent = `${insurance.insurance_type}-${insurance.insurance_id}`
            select.appendChild(option)
        })
    }
    catch (err)
    {
        console.error('Failed to load insurances:', err)
    }
}

fetchInsurances()

function getFurnitureData()
{
    const furnitureData = []

    const fieldsets = document.querySelectorAll('#furniture-container fieldset')


    let allValid = true

    fieldsets.forEach((fieldset) =>
    {
        const sizeInput = fieldset.querySelector('input[name="furniture[][size]"]')
        if (!validateDimensions(sizeInput.value))
        {
            allValid = false
            sizeInput.style.borderColor = 'red'
            alert('Please enter dimensions in the correct format (e.g., 100x120x108)')
        }
        else
        {
            sizeInput.style.borderColor = '' // Reset if valid
        }
    })
    if (!allValid)
    {
        return
    }
    fieldsets.forEach((fieldset) =>
    {

        const sizeInput = fieldset.querySelector(`input[name="furniture[][size]"]`).value
        const dimensions = sizeInput.split('x').map(Number)
        const dimensionsSum = dimensions.reduce((acc, val) => acc + val, 0)


        const furnitureType = fieldset.querySelector(`select[name="furniture[][type]"]`).value

        const material = fieldset.querySelector(`select[name="furniture[][material]"]`).value

        const furniture = {
            "dimensions": dimensionsSum,
            "is_leather": material === 'leather' ? 1 : 0,
            "is_fabric": material === 'fabric' ? 1 : 0,
            "is_none": material === 'none' ? 1 : 0,
            "is_sofa": furnitureType === 'sofa' ? 1 : 0,
            "is_table": furnitureType === 'table' ? 1 : 0,
            "is_chair": furnitureType === 'chair' ? 1 : 0,
        }

        furnitureData.push(furniture)
    })

    const insuranceSelect = document.getElementById('insurance')
    const insuranceValue = insuranceSelect ? insuranceSelect.value : 'basic'

    const insuranceMap = {
        'basic': 0,
        'advanced': 1,
        'full': 2
    }
    const insuranceType = insuranceMap[insuranceValue] || 0
    const result = {
        "furniture_set": furnitureData,
        "insurance_type": insuranceType
    }

    return JSON.stringify(result, null, 2)
}

function validateDimensions(input)
{
    const dimensions = input.split('x')
    return !(dimensions.length !== 3 || dimensions.some(part => isNaN(part)))
}

document.querySelector('.report-event-button').addEventListener('click', async (e) =>
{
    e.preventDefault()
    const jsonData = getFurnitureData()

    if (!jsonData)
    {
        alert('Please fill in all fields correctly.')
        return
    }

    const response = await fetch('/api/report-event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: jsonData
    })

    const responseData = await response.json()
    if (response.ok)
    {
        const messageBox = document.createElement('div')
        messageBox.classList.add('result-box')

        const result = document.createElement('h2')
        result.style.color = 'rgb(66, 35, 115)'
        result.textContent = `Your insurance will cover roughly: ${responseData.result.toFixed(2)}`

        const deviation = document.createElement('p')
        deviation.classList.add('insurance-uuid')
        deviation.textContent = `Expect a deviation of approximately 3000`

        messageBox.appendChild(result)
        messageBox.appendChild(deviation)
        document.body.appendChild(messageBox)
    }
    else
    {
        alert("Something went wrong. Please try again.: " + responseData.error)
    }
})
