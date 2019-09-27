<template>
    <div>
        <div class="d-flex justify-content-center mt-5" v-if="isBusy">
            <strong>Завантаження даних...</strong>
            <b-spinner class="ml-2"></b-spinner>
        </div>

        <b-table-simple small caption-top responsive striped bordered v-else id="statistics-table">
            <caption>Статистичні дані щодо розгляду заявок на реєстрацію АП за період від {{ dateFrom | moment("DD.MM.YYYY") }} до {{ dateTo | moment("DD.MM.YYYY") }}</caption>
            <b-thead class="text-center">
                <b-tr>
                    <b-th rowspan="3">Суб'єкт авторського права, який подав заявку</b-th>
                    <b-th colspan="7">Заявок</b-th>
                    <b-th rowspan="2">Видано свідоцтв</b-th>
                </b-tr>
                <b-tr>
                    <b-th>подано</b-th>
                    <b-th colspan="6">розглянуто</b-th>
                </b-tr>
                <b-tr>
                    <b-th></b-th>
                    <b-th>Зареєстровано</b-th>
                    <b-th>Без розгляду</b-th>
                    <b-th>Відмова</b-th>
                    <b-th>Повернено</b-th>
                    <b-th>Відхилено</b-th>
                    <b-th>ВСЬОГО</b-th>
                    <b-th></b-th>
                </b-tr>
            </b-thead>
            <b-tbody class="text-center">
                <b-tr>
                    <b-td>Фізичні особи</b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'applied_phys')">{{ statistics.applied_phys }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'registered_phys')">{{ statistics.registered_phys }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'without_review_phys')">{{ statistics.without_review_phys }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'refusal_phys')">{{ statistics.refusal_phys }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'return_phys')">{{ statistics.return_phys }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'canceled_phys')">{{ statistics.canceled_phys }}</a></b-td>
                    <b-td>{{ considered_phys_sum }}</b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'issued_phys')">{{ statistics.issued_phys }}</a></b-td>
                </b-tr>
                <b-tr>
                    <b-td>Юридичні особи</b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'applied_jur')">{{ statistics.applied_jur }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'registered_jur')">{{ statistics.registered_jur }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'without_review_jur')">{{ statistics.without_review_jur }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'refusal_jur')">{{ statistics.refusal_jur }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'return_jur')">{{ statistics.return_jur }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'canceled_jur')">{{ statistics.canceled_jur }}</a></b-td>
                    <b-td>{{ considered_jur_sum }}</b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'issued_jur')">{{ statistics.issued_jur }}</a></b-td>
                </b-tr>
                <b-tr>
                    <b-td>Всього</b-td>
                    <b-td>{{ applied_sum }}</b-td>
                    <b-td>{{ registered_sum }}</b-td>
                    <b-td>{{ without_review_sum }}</b-td>
                    <b-td>{{ refusal_sum }}</b-td>
                    <b-td>{{ return_sum }}</b-td>
                    <b-td>{{ canceled_sum }}</b-td>
                    <b-td>{{ considered_sum }}</b-td>
                    <b-td>{{ issued_sum }}</b-td>
                </b-tr>
            </b-tbody>
            <b-tfoot>
                <b-tr>
                    <b-td colspan="9" variant="secondary" class="text-right">
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
                statistics: {
                    // Подано фіз.
                    applied_phys: 0,
                    // Подано юр.
                    applied_jur: 0,
                    // Зареєстровано фіз.
                    registered_phys: 0,
                    // Зареєстровано юр.
                    registered_jur: 0,
                    // Без розгляду фіз.
                    without_review_phys: 0,
                    // Без розгляду юр.
                    without_review_jur: 0,
                    // Відмова фіз.
                    refusal_phys: 0,
                    // Відмова юр.
                    refusal_jur: 0,
                    // Повернено фіз.
                    return_phys: 0,
                    // Повернено юр.
                    return_jur: 0,
                    // Відхилено фіз.
                    canceled_phys: 0,
                    // Відхилено юр.
                    canceled_jur: 0,
                    // Видано фіз.
                    issued_phys: 0,
                    // Видано юр.
                    issued_jur: 0,
                },
            }
        },
        computed: {
            // Всього поданих
            applied_sum() {
                return this.statistics.applied_phys + this.statistics.applied_jur;
            },

            // Всього зареєстровано
            registered_sum() {
                return this.statistics.registered_phys + this.statistics.registered_jur;
            },

            // Всього без розгляду
            without_review_sum() {
                return this.statistics.without_review_phys + this.statistics.without_review_jur;
            },

            // Всього відмова
            refusal_sum() {
                return this.statistics.refusal_phys + this.statistics.refusal_jur;
            },

            // Всього повернено
            return_sum() {
                return this.statistics.return_phys + this.statistics.return_jur;
            },

            // Всього відхилено
            canceled_sum() {
                return this.statistics.canceled_phys + this.statistics.canceled_jur;
            },

            // Всього видано
            issued_sum() {
                return this.statistics.issued_phys + this.statistics.issued_jur;
            },

            // Всього розглянуто фіз.
            considered_phys_sum() {
                return this.statistics.registered_phys
                    + this.statistics.without_review_phys
                    + this.statistics.refusal_phys
                    + this.statistics.return_phys
                    + this.statistics.canceled_phys;
            },

            // Всього розглянуто юр.
            considered_jur_sum() {
                return this.statistics.registered_jur
                    + this.statistics.without_review_jur
                    + this.statistics.refusal_jur
                    + this.statistics.return_jur
                    + this.statistics.canceled_jur;
            },

            // Всього розглянуто
            considered_sum() {
                return this.considered_phys_sum + this.considered_jur_sum;
            }
        },

        created() {
            // Загрузка статистических данных
            this.getStatisticsData();
        },

        methods: {
            getStatisticsData: function () {
                this.isBusy = true;
                axios.get('/api/statistics/ap/', {
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