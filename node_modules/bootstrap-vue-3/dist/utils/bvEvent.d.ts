import { Component } from 'vue';
export declare class BvEvent {
    cancelable: boolean;
    componentId: string | null;
    defaultPrevented: boolean;
    nativeEvent: any;
    preventDefault: () => void;
    relatedTarget: any;
    target: any;
    eventType: string;
    vueTarget: Component | null;
    constructor(eventType: string, eventInit?: {});
    static get Defaults(): {
        eventType: string;
        cancelable: boolean;
        nativeEvent: null;
        target: null;
        relatedTarget: null;
        vueTarget: null;
        componentId: null;
    };
}
