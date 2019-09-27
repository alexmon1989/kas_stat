<template>
    <div>
        <div class="d-flex justify-content-center mt-5" v-if="isBusy">
            <strong>Завантаження даних...</strong>
            <b-spinner class="ml-2"></b-spinner>
        </div>

        <b-table-simple small
                        caption-top
                        responsive
                        striped
                        bordered
                        id="statistics-table"
                        v-else>
            <caption>Статистичні дані щодо навантаження фахівців за період від {{ dateFrom | moment("DD.MM.YYYY") }} до {{ dateTo | moment("DD.MM.YYYY") }}</caption>
            <b-thead class="text-center">
                <b-tr>
                    <b-th rowspan="2">Фахівець</b-th>
                    <b-th colspan="3">Кількість заявок</b-th>
                    <b-th rowspan="2">Середній час розгляду заявок</b-th>
                    <b-th rowspan="2">Кількість реєстрацій</b-th>
                    <b-th rowspan="2">Кількість внесених змін</b-th>
                    <b-th colspan="4">Надходження до бюджету, грн.</b-th>
                </b-tr>
                <b-tr>
                    <b-th>Прийнятих до розгляду</b-th>
                    <b-th>Розглянуті</b-th>
                    <b-th>на розгляді</b-th>
                    <b-th>За підготовку до державної реєстрації</b-th>
                    <b-th>За внесення змін</b-th>
                </b-tr>
            </b-thead>
            <b-tbody class="text-center">
                <b-tr v-for="item in statistics" :key="item.name">
                    <b-td><a href="#" @click.prevent="$emit('show-apps', '', item.name)">{{ item.name }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'applied', item.name)">{{ item.applied }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'reviewed', item.name)">{{ item.reviewed }}</a></b-td>
                    <b-td>{{ item.reviewing }}</b-td>
                    <b-td>{{ item.average_time }}</b-td>
                    <b-td>{{ item.registrations }}</b-td>
                    <b-td>{{ item.changes }}</b-td>
                    <b-td>{{ item.budget_preparing }}</b-td>
                    <b-td>{{ item.budget_changes }}</b-td>
                </b-tr>
                <b-tr>
                    <b-td>Всього</b-td>
                    <b-td>{{ applied_total }}</b-td>
                    <b-td>{{ reviewed_total }}</b-td>
                    <b-td>{{ reviewing_total }}</b-td>
                    <b-td>{{ average_time_total }}</b-td>
                    <b-td>{{ registrations_total }}</b-td>
                    <b-td>{{ changes_total }}</b-td>
                    <b-td>{{ budget_preparing_total }}</b-td>
                    <b-td>{{ budget_changes_total }}</b-td>
                </b-tr>
            </b-tbody>
            <b-tfoot>
                <b-tr>
                    <b-td colspan="12" variant="secondary" class="text-right">
                        <b-button size="sm"
                                  @click="excelExport('statistics-table', 'Статистика', 'statistics.xls')"
                        >Експорт у Excel</b-button>
                    </b-td>
                </b-tr>
            </b-tfoot>
        </b-table-simple>
    </div>
</template>

<script>
    import axios from 'axios';
    import ExcelMixin from './../../mixins/ExcelMixin';

    export default {
        props: ['dateFrom', 'dateTo'],
        mixins: [ExcelMixin],

        data() {
            return {
                isBusy: true,
                statistics: [
                    {
                        name: 'ФІО_1',
                        applied: 0,
                        reviewed: 0,
                        reviewing: 0,
                        average_time: 0,
                        registrations: 0,
                        changes: 0,
                        budget_preparing: 0,
                        budget_changes: 0,
                    }
                ]
            }
        },
        computed: {
            applied_total() {
                return this.statistics.reduce(function (sum, current) {
                    return sum + current.applied;
                }, 0);
            },

            reviewed_total() {
                return this.statistics.reduce(function (sum, current) {
                    return sum + current.reviewed;
                }, 0);
            },

            reviewing_total() {
                return this.statistics.reduce(function (sum, current) {
                    return sum + current.reviewing;
                }, 0);
            },

            average_time_total() {
                return this.statistics.reduce(function (sum, current) {
                    return sum + current.average_time;
                }, 0);
            },

            registrations_total() {
                return this.statistics.reduce(function (sum, current) {
                    return sum + current.registrations;
                }, 0);
            },

            changes_total() {
                return this.statistics.reduce(function (sum, current) {
                    return sum + current.changes;
                }, 0);
            },

            budget_preparing_total() {
                return this.statistics.reduce(function (sum, current) {
                    return sum + current.budget_preparing;
                }, 0);
            },

            budget_changes_total() {
                return this.statistics.reduce(function (sum, current) {
                    return sum + current.budget_changes;
                }, 0);
            }
        },

        created() {
            // Загрузка статистических данных
            this.getStatisticsData();
        },

        methods: {
            getStatisticsData: function () {
                this.isBusy = true;
                axios.get('/api/statistics/dg_specialist_workload_statistics/', {
                    params: {
                        date_from: this.dateFrom.toISOString().split('T')[0],
                        date_to: this.dateTo.toISOString().split('T')[0],
                    }
                }).then(response => {
                    this.statistics = response.data;
                    this.isBusy = false;
                })
            }
        },

        watch: {
            dateFrom() {
                if (!this.isBusy) {
                    this.getStatisticsData();
                }
            },
            dateTo() {
                if (!this.isBusy) {
                    this.getStatisticsData();
                }
            }
        }
    }
</script>