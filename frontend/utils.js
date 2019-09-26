function strip_tags( str ){	// Strip HTML and PHP tags from a string
	return str.replace(/<\/?[^>]+>/gi, '');
}

let tableToExcel = (function () {
    let uri = 'data:application/vnd.ms-excel;base64,'
        ,
        template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--><meta http-equiv="content-type" content="text/plain; charset=UTF-8"/></head><body><table>{table}</table></body></html>'
        , base64 = function (s) {
            return window.btoa(unescape(encodeURIComponent(s)))
        }
        , format = function (s, c) {
            return s.replace(/{(\w+)}/g, function (m, p) {
                return c[p];
            })
        }
        , downloadURI = function (uri, name) {
            let link = document.createElement('a');
            // Add the element to the DOM
            link.setAttribute("type", "hidden"); // make it hidden if needed
            link.download = name;
            link.href = uri;
            document.body.appendChild(link);
            link.click();
            link.remove();
        };

    return function (table, name, fileName) {
        if (!table.nodeType) table = document.getElementById(table);

        let clnTable = table.cloneNode(true);

        // Удаление последней строки
        clnTable.rows[clnTable.rows.length - 1].remove();

        // Удаление тегов из ячеек
        for (let row of clnTable.rows) {
            for (let cell of row.cells) {
                cell.innerText = strip_tags(cell.innerText);
            }
        }

        let ctx = {worksheet: name || 'Worksheet', table: clnTable.innerHTML};
        let resuri = uri + base64(format(template, ctx));
        clnTable.remove();
        downloadURI(resuri, fileName);
    }
})();

export {tableToExcel}
