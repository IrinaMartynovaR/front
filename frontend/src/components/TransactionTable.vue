<template>
<v-data-table
    :headers = "headers"
    :item="transaction"
></v-data-table>
</template>

<script>
export default {
    data() {
        return {
            headers: [
                {text: 'Transaction title', value: 'title'},
                {text: 'Amount', value: 'amount'}
            ],
            transaction: [
            {
                title: 'Заправка "Лукоил"',
                amount: '1562.2 руб'
            },
            {
                title: 'Магазин "Лукошко"',
                amount: '5251.53 руб'
            },
            {
                title: 'Шоколадница',
                amount: '320 руб'
            }
            ]
        }
    }
}
</script>

<style lang="css" scoped></style>