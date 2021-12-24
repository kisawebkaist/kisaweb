const chartOptions = {
    width: 600,
    type: 'pie',
};

const responsiveOptions = [{
    breakpoint: 600,
    options: {
        chart: {
            width: 450
        },
        legend: {
            position: 'bottom'
        },
        dataLabels: {
            enabled: true,
            style: {
                fontSize: "12px",
            }
        }
    }
},
{
    breakpoint: 450,
    options: {
        chart: {
            width: 350
        },
        legend: {
            position: 'bottom'
        },
        dataLabels: {
            enabled: true,
            style: {
                fontSize: "12px",
            }
        }
    }
}
];

var options = {
    series: [],
    chart: chartOptions,
    labels: electionCategories,
    responsive: responsiveOptions
};
var myChartDiv, electionTotalVotes;

const getChartOptions = (chosenOption) => {
    console.log(options);
    if (chosenOption == 'All Votes') {
        options.series = electionAllVotes;
    }
    else if (chosenOption == 'Non-KISA Votes') {
        options.series = electionNonKISAVotes;
    }
    else {
        options.series = electionKISAVotes;
    }
    $(electionTotalVotes).text(options.series.reduce((a, b) => a + b, 0));
    return options;
}

$('.election-dropdown-option').click((e) => {
    console.log(e);
    const chosenOption = e.target.innerText;
    $('#election-dropdown-button').text(chosenOption);
    $(myChartDiv).empty()
    chart = new ApexCharts(myChartDiv, getChartOptions(chosenOption));
    chart.render();
});

$(document).ready(() => {
    myChartDiv = $("#myChart")[0];
    electionTotalVotes = $('#election-total-votes')[0];
    chart = new ApexCharts(myChartDiv, getChartOptions('All Votes'));
    chart.render();
});

