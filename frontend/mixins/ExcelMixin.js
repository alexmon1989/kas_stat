import {tableToExcel} from  './../utils.js'

export default {
    methods: {
        // Экспорт таблицы в Excel
        excelExport: function (table, name, fileName) {
            tableToExcel(table, name, fileName);
        }
    },
}
