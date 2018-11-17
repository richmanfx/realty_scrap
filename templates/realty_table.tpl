<!doctype html>
<html lang="ru">
    <head>
    	<meta charset="utf-8">
        <title>Realty Objects</title>
        <link rel="stylesheet" type="text/css" href="css/real.css">
    </head>


    <body>
    	<h1>Объекты недвижимости</h1>

        <table class="real-table">
            <caption>{{ config_file.PROPERTY_LOCATION }}, {{ config_file.CONTRACT_TYPE }}</caption>
            <tr>
                {% for titles in table_titles %}
                    <th>{{titles}}</th>
                {% endfor %}
            </tr>
            {% for realty_object_string in realty_objects_array %}
            <tr>
                <td>{{realty_object_string[0]}}</td>
                <td><a href="{{realty_object_string[13]}}">{{realty_object_string[1]}}</a></td>
                {% if realty_object_string[2] >= required_profit_margin %}
                    <td class="gud-payback">{{realty_object_string[2]}}</td>
                {% else %}
                    <td class="bad-payback">{{realty_object_string[2]}}</td>
                {% endif %}
                <td>{{realty_object_string[3]}}</td>
                <td>{{realty_object_string[4]}}</td>
                <td>{{realty_object_string[5]}}</td>
                <td>{{realty_object_string[6]}}</td>
                <td>{{realty_object_string[7]}}</td>
                <td>{{realty_object_string[8]}}</td>
                <td>{{realty_object_string[9]}}</td>
                <td>{{realty_object_string[10]}}</td>
                <td>{{realty_object_string[11]}}</td>
                <td>{{realty_object_string[12]}}</td>
            </tr>
            {% endfor %}
        </table>

    <br><br>
        <h1>Основные параметры</h1>

        <h2>Статистические:</h2>
            <ul>
                <li>Средняя стоимость аренды: {{ "%.2f руб/кв.м. в месяц"|format(config_file.AVERAGE_RENTAL) }}</li>
                <li>Количество доходных месяцев в году: {{ "%.0f"|format(config_file.PROFIT_MONTHS) }}</li>
            </ul>

        <h2>Разовые затраты:</h2>
            <ul>
                <li>Стоимость регистрации договора: {{ "%.2f руб."|format(config_file.CONTRACT_REGISTRATION) }}</li>
                <li>Расходы на запуск объекта: {{ "%.2f руб."|format(config_file.RUNNING_COST) }}</li>
            </ul>



        <h2>Расценки:</h2>
            <ul>
                <li>Отопление: {{ "%.2f руб/кв.м. в месяц"|format(config_file.HEATING) }}</li>
                <li>Обслуживание ЖЭКом: {{ "%.2f руб/кв.м. в месяц"|format(config_file.HOUSING_OFFICE) }}</li>
                <li>Бухгалтерское обслуживание: {{ "%.2f руб/мес"|format(config_file.ACCOUNTING_SERVICE) }}</li>
                <li>Предварительный ремонт: {{ "%.2f руб/кв.м."|format(config_file.REPAIR) }}</li>
            </ul>

    </body>
</html>
