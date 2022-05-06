import { ComputedRef } from 'vue';
declare const getClasses: (props: any) => ComputedRef;
declare const getInputClasses: (props: any) => ComputedRef;
declare const getLabelClasses: (props: any) => ComputedRef;
declare const getGroupAttr: (props: any) => ComputedRef;
declare const getGroupClasses: (props: any) => ComputedRef;
declare const slotsToElements: (slots: Array<any>, nodeType: string, disabled: boolean) => {
    props: any;
    text: any;
}[];
declare const optionToElement: (option: any, props: any) => any;
declare const bindGroupProps: (el: any, idx: number, props: any, computedName: ComputedRef, computedId: ComputedRef) => any;
export { getClasses, getInputClasses, getLabelClasses, getGroupAttr, getGroupClasses, slotsToElements, optionToElement, bindGroupProps, };
