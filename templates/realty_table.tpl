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
            <tr>
                {% for titles in table_titles %}
                    <th>{{titles}}</th>
                {% endfor %}
            </tr>
            {% for realty_object_string in realty_objects_array %}
            <tr>
                <td>{{realty_object_string[0]}}</td>
                {% if realty_object_string[1] >= required_profit_margin %}
                    <td class="gud-payback">{{realty_object_string[1]}}</td>
                {% else %}
                    <td class="bad-payback">{{realty_object_string[1]}}</td>
                {% endif %}
                <td>{{realty_object_string[2]}}</td>
                <td>{{realty_object_string[3]}}</td>
                <td>{{realty_object_string[4]}}</td>
                <td>{{realty_object_string[5]}}</td>
                <td>{{realty_object_string[6]}}</td>
                <td>{{realty_object_string[7]}}</td>
                <td>{{realty_object_string[8]}}</td>
                <td>{{realty_object_string[9]}}</td>
                <td>{{realty_object_string[10]}}</td>
                <td>{{realty_object_string[11]}}</td>
            </tr>
            {% endfor %}
        </table>

    </body>
</html>
