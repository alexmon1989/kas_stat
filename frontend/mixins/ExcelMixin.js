import {tableToExcel} from  './../utils.js'

export default {
    methods: {
        // Экспорт таблицы в Excel
        excelExport: function (table, name, fileName, removeLastTr) {
            tableToExcel(table, name, fileName, removeLastTr);
        }
    },
}
