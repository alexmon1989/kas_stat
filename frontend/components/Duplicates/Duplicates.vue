<template>
    <b-container fluid>
        <date-form v-on:send-date-form="onShowStatistics"></date-form>

        <statistics-table v-if="dateFrom && dateTo"
                          :date-from="dateFrom"
                          :date-to="dateTo"
        ></statistics-table>
    </b-container>
</template>

<script>
    import DateForm from './DateForm.vue';
    import StatisticsTable from './StatisticsTable.vue';

    export default {
        data() {
            return {
                dateFrom: '',
                dateTo: '',
            }
        },

        components: {
            DateForm,
            StatisticsTable
        },

        methods: {
            onShowStatistics: function (dateFrom, dateTo) {
                this.dateFrom = '';
                this.dateTo = '';

                this.$nextTick(function () {
                    this.dateFrom = dateFrom;
                    this.dateTo = dateTo;
                });
            }
        },
    }
</script>

<style scoped>

</style>