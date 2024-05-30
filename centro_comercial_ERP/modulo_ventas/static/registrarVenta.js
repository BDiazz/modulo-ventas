document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.add-service-button').addEventListener('click', showServiceModal);
    document.getElementById('venta-form').addEventListener('submit', submitForm);
  });
  
  function showServiceModal() {
    fetch('/agregarServicio/')
      .then(response => response.json())
      .then(data => {
        const serviceSelect = document.getElementById('servicio-select');
        serviceSelect.innerHTML = '';
        data.forEach(service => {
          const option = document.createElement('option');
          option.value = service.id;
          option.text = service.nombre;
          serviceSelect.appendChild(option);
        });
  
        fetch(`/getPeriodos/${serviceSelect.value}/`)
          .then(response => response.json())
          .then(periodos => {
            const periodoSelect = document.getElementById('periodo-select');
            periodoSelect.innerHTML = '';
            periodos.forEach(periodo => {
              const option = document.createElement('option');
              option.value = periodo.id;
              option.text = periodo.tipo;
              periodoSelect.appendChild(option);
            });
          });
      });
  
    document.getElementById('service-modal').style.display = 'block';
  }
  
  function closeServiceModal() {
    document.getElementById('service-modal').style.display = 'none';
  }
  
  function addService() {
    const servicioId = document.getElementById('servicio-select').value;
    const cantidad = document.getElementById('cantidad').value;
    const periodoId = document.getElementById('periodo-select').value;
  
    fetch('/agregarServicio/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({
        servicio_id: servicioId,
        cantidad: cantidad,
        periodo_id: periodoId
      })
    })
    .then(response => response.json())
    .then(data => {
      const table = document.getElementById('servicios-table').getElementsByTagName('tbody')[0];
      const row = table.insertRow();
      row.insertCell(0).innerText = data.servicio;
      row.insertCell(1).innerText = data.precio;
      row.insertCell(2).innerText = data.periodo;
      row.insertCell(3).innerText = data.cantidad;
      row.insertCell(4).innerText = data.subtotal;
      const deleteButton = document.createElement('button');
      deleteButton.type = 'button';
      deleteButton.innerText = 'Eliminar';
      deleteButton.className = 'delete-button';
      deleteButton.onclick = function() {
        row.remove();
      };
      row.insertCell(5).appendChild(deleteButton);
      
      updateTotal();
    });
  }
  
  function updateTotal() {
    const table = document.getElementById('servicios-table').getElementsByTagName('tbody')[0];
    let total = 0;
    for (let i = 0; i < table.rows.length; i++) {
      total += parseFloat(table.rows[i].cells[4].innerText);
    }
    document.getElementById('total').innerText = total.toFixed(2);
  }
  
  function submitForm(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const servicios = [];
    const table = document.getElementById('servicios-table').getElementsByTagName('tbody')[0];
    for (let i = 0; i < table.rows.length; i++) {
      const servicioId = table.rows[i].cells[0].innerText;
      const cantidad = table.rows[i].cells[3].innerText;
      const periodoId = table.rows[i].cells[2].innerText;
      servicios.push({ servicio_id: servicioId, cantidad: cantidad, periodo_id: periodoId });
    }
    formData.append('servicios', JSON.stringify(servicios));
  
    fetch('/registrarVenta/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    })
    .then(response => {
      if (response.ok) {
        return response.json();
      }
      throw new Error('Error al registrar la venta');
    })
    .then(data => {
      // Manejar la respuesta, redireccionar o mostrar un mensaje de éxito
      console.log('Venta registrada con éxito:', data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }
  