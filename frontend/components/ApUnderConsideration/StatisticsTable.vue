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
                    <b-th rowspan="2">подано</b-th>
                    <b-th colspan="5">розглянуто</b-th>
                    <b-th rowspan="2">На розгляді</b-th>
                </b-tr>
                <b-tr>
                    <b-th>Зареєстровано</b-th>
                    <b-th>Без розгляду</b-th>
                    <b-th>Відмова</b-th>
                    <b-th>Повернено</b-th>
                    <b-th>Відхилено</b-th>
                    <b-th></b-th>
                </b-tr>
            </b-thead>
            <b-tbody class="text-center">
                <b-tr>
                    <b-td>Фізичні особи</b-td>
                    <b-td :class="{ 'bg-info text-white': appType === 'applied_phys' }">
                        <a href="#" @click.prevent="$emit('show-apps', 'applied_phys')">{{ statistics.applied_phys }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': appType === 'registered_phys' }">
                        <a href="#" @click.prevent="$emit('show-apps', 'registered_phys')">{{ statistics.registered_phys }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': appType === 'without_review_phys' }">
                        <a href="#" @click.prevent="$emit('show-apps', 'without_review_phys')">{{ statistics.without_review_phys }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': appType === 'refusal_phys' }">
                        <a href="#" @click.prevent="$emit('show-apps', 'refusal_phys')">{{ statistics.refusal_phys }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': appType === 'return_phys' }">
                        <a href="#" @click.prevent="$emit('show-apps', 'return_phys')">{{ statistics.return_phys }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': appType === 'canceled_phys' }">
                        <a href="#" @click.prevent="$emit('show-apps', 'canceled_phys')">{{ statistics.canceled_phys }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': appType === 'under_consideration_phys' }">
                        <a href="#" @click.prevent="$emit('show-apps', 'under_consideration_phys')">{{ statistics.under_consideration_phys }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': appType === 'issued_phys' }">
                        <a href="#" @click.prevent="$emit('show-apps', 'issued_phys')">{{ statistics.issued_phys }}</a>
                    </b-td>
                </b-tr>
                <b-tr>
                    <b-td>Юридичні особи</b-td>
                    <b-td :class="{ 'bg-info text-white': appType === 'applied_jur' }">
                        <a href="#" @click.prevent="$emit('show-apps', 'applied_jur')">{{ statistics.applied_jur }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': appType === 'registered_jur' }">
                        <a href="#" @click.prevent="$emit('show-apps', 'registered_jur')">{{ statistics.registered_jur }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': appType === 'without_review_jur' }">
                        <a href="#" @click.prevent="$emit('show-apps', 'without_review_jur')">{{ statistics.without_review_jur }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': appType === 'refusal_jur' }">
                        <a href="#" @click.prevent="$emit('show-apps', 'refusal_jur')">{{ statistics.refusal_jur }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': appType === 'return_jur' }">
                        <a href="#" @click.prevent="$emit('show-apps', 'return_jur')">{{ statistics.return_jur }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': appType === 'canceled_jur' }">
                        <a href="#" @click.prevent="$emit('show-apps', 'canceled_jur')">{{ statistics.canceled_jur }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': appType === 'under_consideration_jur' }">
                        <a href="#" @click.prevent="$emit('show-apps', 'under_consideration_jur')">{{ statistics.under_consideration_jur }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': appType === 'issued_jur' }">
                        <a href="#" @click.prevent="$emit('show-apps', 'issued_jur')">{{ statistics.issued_jur }}</a>
                    </b-td>
                </b-tr>
                <b-tr>
                    <b-td>Всього</b-td>
                    <b-td>{{ applied_sum }}</b-td>
                    <b-td>{{ registered_sum }}</b-td>
                    <b-td>{{ without_review_sum }}</b-td>
                    <b-td>{{ refusal_sum }}</b-td>
                    <b-td>{{ return_sum }}</b-td>
                    <b-td>{{ canceled_sum }}</b-td>
                    <b-td>{{ under_consideration_sum }}</b-td>
                    <b-td>{{ issued_sum }}</b-td>
                </b-tr>
            </b-tbody>
            <b-tfoot>
                <b-tr>
                    <b-td colspan="9" variant="secondary" class="text-right">
                        <b-button size="sm"
                                  @click="excelExport('statistics-table', 'Статистика', 'statistics.xls')"
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
        props: ['dateFrom', 'dateTo', 'appType'],
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
                    // На розгляді фіз.
                    under_consideration_phys: 0,
                    // На розгляді юр.
                    under_consideration_jur: 0,
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

            // Всього на розгляді
            under_consideration_sum() {
                return this.statistics.under_consideration_phys + this.statistics.under_consideration_jur;
            }
        },

        created() {
            // Загрузка статистических данных
            this.getStatisticsData();
        },

        methods: {
            getStatisticsData: function () {
                this.isBusy = true;
                axios.get('/api/statistics/ap_under_consideration/', {
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