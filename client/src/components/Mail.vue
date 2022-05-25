<script setup>
import { ref } from 'vue'
//import Message from flask_mail

const sender = ref('')
const receiving = ref('')
const message = ref('')
</script>


<template>
    <b-container>
        <h2 class="text-center">Sending a mail</h2>
        <b-row>
            <b-col>
                <h6>Sender:</h6>
                <b-form-input
                    v-model="sender"
                    type="email"
                />
            </b-col>
            <b-col>
                <h6>Receiver:</h6>
                <b-form-input
                    v-model="receiving"
                    type="email"
                />
            </b-col>
            <b-col>
            </b-col>
        </b-row>
        <h6>Message:</h6>
        <b-row>
            <b-form-input
                v-model="message"
                type="text"
            />
        </b-row>
    </b-container>
</template>