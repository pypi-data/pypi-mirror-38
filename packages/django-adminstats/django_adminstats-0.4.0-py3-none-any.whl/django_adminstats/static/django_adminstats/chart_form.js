(function($) {
    function findField(name, fieldType, parent=null) {
        var spec = ('.field-' + name + ' ' + fieldType
                    + ', .grp-row.' + name + ' ' + fieldType);
        if (parent===null) return $(spec);
        return parent.find(spec);
    }

    function findFieldRow(name, parent=null) {
        var spec = ('.field-' + name + ', .grp-row.' + name);
        if (parent===null) return $(spec);
        return parent.find(spec);
    }

    function selectUntilType(elem) {
        var opt = elem.options[elem.selectedIndex];
        findFieldRow('until_date').toggle(opt.value == 's');
    }

    document.addEventListener('DOMContentLoaded', function() {
        untilTypeField = findField('until_type', 'select');
        untilTypeField.on('change', function() {selectUntilType(this)});
        selectUntilType(untilTypeField[0]);
    });
})(django.jQuery)
