<template>
    <v-app id="inspire">
        <v-navigation-drawer v-model="drawer" app right>
            <v-list dense>
                <v-list-item link>
                    <v-list-item-action>
                        <v-icon>mdi-home</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Home</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                </v-list-item link>
                    <v-list-item-action>
                        <v-icon>mdi-contact-mail</v-icon>
                    </v-list-item-action>
                    </v-list-item-content>
                        <v-list-item-title>Contact</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>
        <v-app-bar app color="primary" dark>
            <v-spacer />
            <v-toolbar-title> Frontend application</v-toolbar-title>
            <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
        </v-app-bar>
        <v-content>
            <slot />
        </v-content>
        <v-footer color="primary" app>
            <v-spacer />
            <span class="white--text">&copy; 2019</span>
        </v-footer>
    </v-app>
</template>