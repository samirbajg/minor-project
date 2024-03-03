const cdata = data

const labels = ['Anger', 'Love', 'Fear', 'Joy', 'Sadness', 'Surprise'];
  const chartData = {
    labels: labels,
    datasets: [{
      data: cdata,
      backgroundColor: [
        '#910513', // Anger
        'rgb(248, 114, 136)', // Love
        '#000000', // Fear
        '#ffc107', // Joy
        '#007bff', // Sadness
        'cyan', // Surprise
      ]
    }]
  };

const ctx = document.getElementById('sentimentChart').getContext('2d');
const sentimentChart = new Chart(ctx, {
  type: 'pie',
  data: chartData
});
