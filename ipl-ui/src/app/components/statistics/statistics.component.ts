import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { NgxSpinnerService } from 'ngx-spinner';
import * as Highcharts from 'highcharts';
Highcharts.setOptions({
  chart: {
    resetZoomButton: {
      theme: {
        zIndex: 8,
      },
    },
  },
  boost: {
    useGPUTranslations: true,
  },
  lang: {
    decimalPoint: '.',
    thousandsSep: ',',
    drillUpText: '< back',
  },
  exporting: {
    enabled: false,
    fallbackToExportServer: false,
  },
  title: {
    text: '',
  },
  credits: {
    enabled: false,
  },
  scrollbar: {
    barBackgroundColor: 'gray',
    barBorderRadius: 7,
    barBorderWidth: 0,
    buttonBackgroundColor: 'gray',
    buttonBorderWidth: 0,
    buttonBorderRadius: 7,
    trackBackgroundColor: 'none',
    trackBorderWidth: 1,
    trackBorderRadius: 8,
    trackBorderColor: '#CCC',
  },

  tooltip: {
    shadow: false,
    borderWidth: 1,
    borderColor: '#c0c0c0',
    shared: true,
  },
});
@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.scss'],
})
export class StatisticsComponent implements OnInit {
  constructor(private http: HttpClient, private spinner: NgxSpinnerService) {}
  Highcharts = Highcharts;
  columnChart = {
    chart: {
      type: 'column',
    },
    xAxis: {
      categories: [],
      crosshair: true,
    },
    yAxis: {
      title: {
        text: 'Runs',
      },
    },
    plotOptions: {
      column: {
        dataLabels: {
          enabled: true,
        },
      },
    },
    series: [
      {
        name: 'Players',
        color: '#19398a',
        data: [],
      },
    ],
  };
  barChart = {
    chart: {
      type: 'bar',
    },
    xAxis: {
      categories: [],
      crosshair: true,
    },
    yAxis: {
      title: {
        text: 'Wickets',
      },
    },
    plotOptions: {
      bar: {
        dataLabels: {
          enabled: true,
        },
      },
    },
    series: [
      {
        name: 'Players',
        color: '#19398a',
        data: [],
      },
    ],
  };
  pieChart = {
    chart: {
      plotBackgroundColor: null,
      plotBorderWidth: null,
      plotShadow: false,
      type: 'pie',
    },
    tooltip: {
      pointFormat:
        '{series.name}: <br>{point.percentage:.1f} %<br>wins: {point.y}',
    },
    accessibility: {
      point: {
        valueSuffix: '%',
      },
    },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: 'pointer',
        dataLabels: {
          enabled: true,
          format: '<b>{point.name}</b><br>wins: {point.y}',
        },
      },
    },
    series: [
      {
        name: 'Teams',
        colorByPoint: true,
        data: [],
      },
    ],
  };
  // baseheader = 'http://localhost:8000/';
  baseheader = '/';
  urls = ['ipl/seasons/', 'ipl/statistics/', 'ipl/charts/'];
  seasons = [];
  selectedSeason = '';
  statistics = {};
  getRequest<T>(url: string, params?: object) {
    return this.http.post<T>(url, params);
  }
  unsorted() {}

  ngOnInit(): void {
    this.spinner.show('spinner_stat');
    this.spinner.show('spinner_ccr');
    this.spinner.show('spinner_bcw');
    this.spinner.show('spinner_pcw');
    this.getRequest(this.baseheader + this.urls[0]).subscribe((data) => {
      if (!data.hasOwnProperty('error')) {
        this.seasons = data['seasons'];
        this.selectedSeason = this.seasons[0];
        this.getStatistics();
        this.getChartData();
      }
    });
  }

  getStatistics() {
    this.spinner.show('spinner_stat');

    this.getRequest(this.baseheader + this.urls[1], {
      season: this.selectedSeason,
    }).subscribe((data) => {
      if (!data.hasOwnProperty('error')) {
        this.statistics = {
          'Top 4 teams': data['top_4'],
          'Team winning maximum number of the matches': data['won_max_mat'],
          'Most number of Man of the Matches award': data['max_mom'],
          'Team won with the highest margins of runs':
            data['highest_margin_run'],
          'Team won with the highest margins of wickets':
            data['highest_margin_wickets'],
          'Player who took most number of catches in a match':
            data['most_catches'],
          'Team winning most number of tosses': data['most_tosses_won'],
          '% of teams choosing to bat after winning the toss':
            data['per_won_toss'],
          'Times a team winning both toss and match': data['won_toss_match'],
          'Venue hosting most number of matches': data['max_hosted_venue'],
          'Venue hosting most number of matches for the top team':
            data['max_hosted_venue_top_team'],
        };
        this.spinner.hide('spinner_stat');
      }
      this.spinner.hide('spinner_stat');
    });
  }

  getChartData() {
    this.spinner.show('spinner_ccr');
    this.spinner.show('spinner_bcw');
    this.spinner.show('spinner_pcw');

    this.getRequest(this.baseheader + this.urls[2], {
      season: this.selectedSeason,
    }).subscribe((data) => {
      if (!data.hasOwnProperty('error')) {
        // total runs
        this.columnChart['xAxis']['categories'] = [];
        this.columnChart['series'][0]['data'] = [];

        for (let i = 0; i < data['by_runs'].length; i++) {
          this.columnChart['xAxis']['categories'].push(
            data['by_runs'][i]['batsman']
          );
          this.columnChart['series'][0]['data'].push(
            data['by_runs'][i]['runs']
          );
        }
        let columnChart_runs = document.getElementById(
          'columnChart_runs'
        ) as HTMLElement;
        (<any>Highcharts).chart(columnChart_runs, this.columnChart);
        this.spinner.hide('spinner_ccr');

        // total wickets
        this.barChart['xAxis']['categories'] = [];
        this.barChart['series'][0]['data'] = [];
        for (let i = 0; i < data['by_wickets'].length; i++) {
          this.barChart['xAxis']['categories'].push(
            data['by_wickets'][i]['bowler']
          );
          this.barChart['series'][0]['data'].push(
            data['by_wickets'][i]['wickets']
          );
        }
        let barChart_wickets = document.getElementById(
          'barChart_wickets'
        ) as HTMLElement;
        (<any>Highcharts).chart(barChart_wickets, this.barChart);
        this.spinner.hide('spinner_bcw');

        // total wins
        this.pieChart['series'][0]['data'] = [];
        for (let i = 0; i < data['by_teams'].length; i++) {
          this.pieChart['series'][0]['data'].push({
            name: data['by_teams'][i]['team'],
            y: data['by_teams'][i]['won'],
            sliced: i == 0 ? true : false,
            selected: i == 0 ? true : false,
          });
        }
        let pieChart_wins = document.getElementById(
          'pieChart_wins'
        ) as HTMLElement;
        (<any>Highcharts).chart(pieChart_wins, this.pieChart);

        this.spinner.hide('spinner_pcw');
      }

      this.spinner.hide('spinner_ccr');
      this.spinner.hide('spinner_bcw');
      this.spinner.hide('spinner_pcw');
    });
  }
}
