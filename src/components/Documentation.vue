<script>
    /*This program has been developed by students from the bachelor Computer Science at
    Utrecht University within the Software Project course.
    © Copyright Utrecht University (Department of Information and Computing Sciences)*/
</script>

<template>
    <div class="text-center my-5">
        <h1>Documentation</h1>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea.</p>
    </div>


    <div>
        <b-card no-body>
            <b-tabs card>
                <!-- Render Tabs, supply a unique `key` to each tab -->
                <b-tab v-for="tab in tabs" :key="tab.id" :class="{active:tab.isActive}" :title="'Tab ' + tab.id">
                Tab contents {{ tab.id }}
                <b-button size="sm" variant="danger" class="float-right" @click="closeTab(tab.id)">
                    Close tab
                </b-button>
                </b-tab>

                <!-- New Tab Button (Using tabs-end slot) -->
                <template v-slot:tabs-end>
                <b-nav-item role="presentation" @click.prevent="newTab" href="#"><b>+</b></b-nav-item>
                </template>

                <!-- Render this if no tabs -->
                <template v-slot:empty>
                <div class="text-center text-muted">
                    There are no open tabs<br>
                    Open a new tab using the <b>+</b> button above.
                </div>
                </template>
            </b-tabs>
        </b-card>
    </div>
</template>


