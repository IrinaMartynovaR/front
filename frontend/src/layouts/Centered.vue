<template>
    <v-app>
        <v-content>
            <v-container fluid fill-height>
                <v-layout align-center justify-center>
                    <v-flex xs12 sm10 md7 lg5>
                        <slot />
                    </v-flex>
                <v-layout>
            </v-container>
        </v-content>
    </v-app>
</template>

<script>
export default {}
</script>

<style lang="css" scoped></style>
