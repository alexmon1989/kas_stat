<template>
    <b-table-simple small caption-top responsive striped bordered id="statistics-table">
        <caption>Реєстр адмінпослуг: "за державну реєстрацію договорів", період: від {{ dateFrom | moment("DD.MM.YYYY") }} до {{ dateTo | moment("DD.MM.YYYY") }}</caption>
        <b-thead class="text-center">
            <b-tr>
                <b-th rowspan="2">№ з/п</b-th>
                <b-th rowspan="2">Найменування отримувача послуг (суб'єкт авторського права (заявник))</b-th>
                <b-th rowspan="2">Код згідно з ЄДРПОУ / ІНН</b-th>
                <b-th rowspan="2">Дата надання адмінпослуги</b-th>
                <b-th colspan="2">Документ, що підтверджує оплату (квітанція)</b-th>
                <b-th rowspan="2">Сума оплати, грн.</b-th>
                <b-th rowspan="2">Переплата</b-th>
                <b-th rowspan="2">REF (з виписки)</b-th>
            </b-tr>
            <b-tr>
                <b-th>номер</b-th>
                <b-th>дата</b-th>
            </b-tr>
        </b-thead>
        <b-tbody class="text-center">
            <b-tr v-for="item in statistics">
                <b-td>{{ item.number }}</b-td>
                <b-td>{{ item.subject }}</b-td>
                <b-td>{{ item.inn }}</b-td>
                <b-td>{{ item.date }}</b-td>
                <b-td>{{ item.document.number }}</b-td>
                <b-td>{{ item.document.date }}</b-td>
                <b-td>{{ item.payment }}</b-td>
                <b-td>{{ item.overpayment }}</b-td>
                <b-td>{{ item.ref }}</b-td>
            </b-tr>
        </b-tbody>
        <b-tfoot>
            <b-tr>
                <b-td colspan="10" variant="secondary" class="text-right">
                    <b-button size="sm"
                              @click="excelExport('statistics-table', 'Статистика', 'statistics.xls')"
                    ><i class="fa fa-file-excel-o mr-2"></i>Експорт у Excel</b-button>
                </b-td>
            </b-tr>
        </b-tfoot>
    </b-table-simple>
</template>

<script>
    import ExcelMixin from './../../mixins/ExcelMixin';

    export default {
        props: ['dateFrom', 'dateTo'],
        mixins: [ExcelMixin],
        data() {
            return {
                statistics: [
                    {
                        number: 1,
                        subject: 'Іванов',
                        inn: '-',
                        date: '-',
                        document: {
                            number: '-',
                            date: '-'
                        },
                        payment: '-',
                        overpayment: '-',
                        ref: '-'
                    },
                    {
                        number: 2,
                        subject: 'Іванов',
                        inn: '-',
                        date: '-',
                        document: {
                            number: '-',
                            date: '-'
                        },
                        payment: '-',
                        overpayment: '-',
                        ref: '-'
                    },
                    {
                        number: 3,
                        subject: 'Іванов',
                        inn: '-',
                        date: '-',
                        document: {
                            number: '-',
                            date: '-'
                        },
                        payment: '-',
                        overpayment: '-',
                        ref: '-'
                    },
                ]
            }
        }
    }
</script>

<style scoped>

</style>