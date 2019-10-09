<template>
    <b-form inline>
        <label class="mr-sm-2">Реєстр адмінпослуг</label>
        <b-form-select class="mb-2 mr-sm-2 mb-sm-0"
                       v-model="registry"
                       :options="registries"></b-form-select>
        <label class="mr-sm-2">З</label>
        <date-picker class="mb-2 mr-sm-2 mb-sm-0"
                     v-model="from"
                     format="DD.MM.YYYY"
                     :lang="lang"
                     :first-day-of-week="1"
        ></date-picker>
        <label class="mr-sm-2">по</label>
        <date-picker class="mb-2 mr-sm-2 mb-sm-0"
                     v-model="to"
                     format="DD.MM.YYYY"
                     :lang="lang"
                     :first-day-of-week="1"
        ></date-picker>
        <b-button variant="primary" @click="$emit('send-date-form', from, to, registry)"><i class="fa fa-search mr-2"></i>Завантажити</b-button>
    </b-form>
</template>

<script>
    import DatePicker from 'vue2-datepicker';
    import DateFormMixin from './../../mixins/DateFormMixin';

    export default {
        components: {DatePicker},
        mixins: [DateFormMixin],
        data() {
            return {
                from: '',
                to: '',
                registry: '',
                registries: [
                    {value: 'За підготовку до державної реєстрації', text: 'За підготовку до державної реєстрації'},
                    {value: 'За видачу свідоцтв', text: 'За видачу свідоцтв'},
                    {value: 'За державну реєстрацію договорів', text: 'За державну реєстрацію договорів'},
                    {value: 'За видачу дубліката свідоцтва', text: 'За видачу дубліката свідоцтва'},
                    {value: 'За внесення змін', text: 'За внесення змін'},
                ],
                lang: {
                    days: [
                        'Нд',
                        'Пн',
                        'Вт',
                        'Ср',
                        'Чт',
                        'Пт',
                        'Сб'
                    ],
                    months: [
                        'Січень',
                        'Лютий',
                        'Березень',
                        'Квітень',
                        'Травень',
                        'Червень',
                        'Липень',
                        'Серпень',
                        'Вересень',
                        'Жовтень',
                        'Листопад',
                        'Грудень'
                    ],
                    pickers: [
                        'наступні 7 днів',
                        'наступні 30 днів',
                        'попередні 7 днів',
                        'попередні 30 днів'
                    ],
                    placeholder: {
                        date: 'Оберіть дату',
                        dateRange: 'Оберіть діапазон дат'
                    }
                }
            }
        },

        methods: {
            onKeyUp(e) {
                if (e.which === 13) {
                    this.$emit('send-date-form', this.from, this.to, this.registry);
                }
            }
        },
    }
</script>