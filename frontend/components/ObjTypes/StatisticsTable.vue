<template>
    <div>
        <div class="d-flex justify-content-center mt-5" v-if="isBusy">
            <strong>Завантаження даних...</strong>
            <b-spinner class="ml-2"></b-spinner>
        </div>

        <b-table-simple small caption-top responsive striped bordered v-else id="statistics-table">
            <caption>Статистичні дані за видом об'єкта за період від {{ dateFrom | moment("DD.MM.YYYY") }} до {{ dateTo | moment("DD.MM.YYYY") }}</caption>
            <b-thead class="text-center">
                <b-tr>
                    <b-th rowspan="2">Вид об’єкта</b-th>
                    <b-th colspan="3">Кількість поданих заяв</b-th>
                    <b-th colspan="3">Кількість реєстрацій</b-th>
                </b-tr>
                <b-tr>
                    <b-th>АП</b-th>
                    <b-th>ДГ</b-th>
                    <b-th>Σ</b-th>
                    <b-th>АП</b-th>
                    <b-th>ДГ</b-th>
                    <b-th>Σ</b-th>
                </b-tr>
            </b-thead>
            <b-tbody class="text-center">
                <b-tr v-for="item in statistics" :key="item.obj_type">
                    <b-td>{{ item.obj_type }}</b-td>
                    <b-td :class="{ 'bg-info text-white': objType === item.obj_type && appType === 'claims_ap'}">
                        <a href="#" @click.prevent="$emit('show-apps', item.obj_type, 'claims_ap')">{{ item.claims.ap }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': objType === item.obj_type && appType === 'claims_dg'}">
                        <a href="#" @click.prevent="$emit('show-apps', item.obj_type, 'claims_dg')">{{ item.claims.dg }}</a>
                    </b-td>
                    <b-td>{{ getClaimsTotal(item) }}</b-td>
                    <b-td :class="{ 'bg-info text-white': objType === item.obj_type && appType === 'registrations_ap'}">
                        <a href="#" @click.prevent="$emit('show-apps', item.obj_type, 'registrations_ap')">{{ item.registrations.ap }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': objType === item.obj_type && appType === 'registrations_dg'}">
                        <a href="#" @click.prevent="$emit('show-apps', item.obj_type, 'registrations_dg')">{{ item.registrations.dg }}</a>
                    </b-td>
                    <b-td>{{ getRegistrationsTotal(item) }}</b-td>
                </b-tr>
            </b-tbody>
            <b-tfoot>
                <b-tr>
                    <b-td colspan="7" variant="secondary" class="text-right">
                        <b-button size="sm"
                                  @click="excelExport('statistics-table', 'Статистика', 'obj_types.xls')"
                        ><i class="fa fa-file-excel-o mr-2"></i>Експорт у Excel</b-button>
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
        props: ['dateFrom', 'dateTo', 'appType', 'objType'],
        mixins: [ExcelMixin],

        data() {
            return {
                isBusy: true,
            }
        },

        created() {
            // Загрузка статистических данных
            this.getStatisticsData();
        },

        methods: {
            getStatisticsData: function () {
                this.isBusy = true;
                axios.get('/api/statistics/obj_types/', {
                    params: {
                        date_from: this.dateFrom.toISOString().split('T')[0],
                        date_to: this.dateTo.toISOString().split('T')[0],
                    }
                }).then(response => {
                    this.statistics = response.data;
                    this.isBusy = false;
                })
            },

            getClaimsTotal: function (item) {
                return item.claims.ap +  item.claims.dg;
            },

            getRegistrationsTotal: function (item) {
                return item.registrations.ap +  item.registrations.dg;
            },
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