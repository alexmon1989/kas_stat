<template>
    <b-form inline>
        <label class="mr-sm-2">З</label>
        <date-picker class="mb-2 mr-sm-2 mb-sm-0"
                     v-model="from"
                     format="DD.MM.YYYY"
                     :lang="lang"
                     :first-day-of-week="1"
                     @keyup.enter.native="$emit('send-date-form', from, to)"
        ></date-picker>
        <label class="mr-sm-2">по</label>
        <date-picker class="mb-2 mr-sm-2 mb-sm-0"
                     v-model="to"
                     format="DD.MM.YYYY"
                     :lang="lang"
                     :first-day-of-week="1"
                     @keyup.enter.native="$emit('send-date-form', from, to)"
        ></date-picker>
        <b-button variant="primary" @click="$emit('send-date-form', from, to)"><i class="fa fa-search mr-2"></i>Завантажити</b-button>
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


    }
</script>