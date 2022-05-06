import { PropType } from 'vue';
import { Alignment, InputSize } from '../../types';
declare const _sfc_main: import("vue").DefineComponent<{
    align: {
        type: PropType<Alignment>;
        default: string;
    };
    ariaControls: {
        type: StringConstructor;
        required: false;
    };
    ariaLabel: {
        type: StringConstructor;
        default: string;
    };
    disabled: {
        type: BooleanConstructor;
        default: boolean;
    };
    ellipsisClass: {
        type: (StringConstructor | ArrayConstructor)[];
        default: () => never[];
    };
    ellipsisText: {
        type: StringConstructor;
        default: string;
    };
    firstClass: {
        type: (StringConstructor | ArrayConstructor)[];
        default: () => never[];
    };
    firstNumber: {
        type: BooleanConstructor;
        default: boolean;
    };
    firstText: {
        type: StringConstructor;
        default: string;
    };
    hideEllipsis: {
        type: BooleanConstructor;
        default: boolean;
    };
    hideGotoEndButtons: {
        type: BooleanConstructor;
        default: boolean;
    };
    labelFirstPage: {
        type: StringConstructor;
        default: string;
    };
    labelLastPage: {
        type: StringConstructor;
        default: string;
    };
    labelNextPage: {
        type: StringConstructor;
        default: string;
    };
    labelPage: {
        type: StringConstructor;
        default: string;
    };
    labelPrevPage: {
        type: StringConstructor;
        default: string;
    };
    lastClass: {
        type: (StringConstructor | ArrayConstructor)[];
        default: () => never[];
    };
    lastNumber: {
        type: BooleanConstructor;
        default: boolean;
    };
    lastText: {
        type: StringConstructor;
        default: string;
    };
    limit: {
        type: NumberConstructor;
        default: number;
    };
    modelValue: {
        type: NumberConstructor;
        default: number;
    };
    nextClass: {
        type: (StringConstructor | ArrayConstructor)[];
        default: () => never[];
    };
    nextText: {
        type: StringConstructor;
        default: string;
    };
    pageClass: {
        type: (StringConstructor | ArrayConstructor)[];
        default: () => never[];
    };
    perPage: {
        type: NumberConstructor;
        default: number;
    };
    pills: {
        type: BooleanConstructor;
        default: boolean;
    };
    prevClass: {
        type: (StringConstructor | ArrayConstructor)[];
        default: () => never[];
    };
    prevText: {
        type: StringConstructor;
        default: string;
    };
    size: {
        type: PropType<InputSize>;
        required: false;
    };
    totalRows: {
        type: NumberConstructor;
        default: number;
    };
}, () => import("vue").VNode<import("vue").RendererNode, import("vue").RendererElement, {
    [key: string]: any;
}>, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, ("update:modelValue" | "page-click")[], "update:modelValue" | "page-click", import("vue").VNodeProps & import("vue").AllowedComponentProps & import("vue").ComponentCustomProps, Readonly<import("vue").ExtractPropTypes<{
    align: {
        type: PropType<Alignment>;
        default: string;
    };
    ariaControls: {
        type: StringConstructor;
        required: false;
    };
    ariaLabel: {
        type: StringConstructor;
        default: string;
    };
    disabled: {
        type: BooleanConstructor;
        default: boolean;
    };
    ellipsisClass: {
        type: (StringConstructor | ArrayConstructor)[];
        default: () => never[];
    };
    ellipsisText: {
        type: StringConstructor;
        default: string;
    };
    firstClass: {
        type: (StringConstructor | ArrayConstructor)[];
        default: () => never[];
    };
    firstNumber: {
        type: BooleanConstructor;
        default: boolean;
    };
    firstText: {
        type: StringConstructor;
        default: string;
    };
    hideEllipsis: {
        type: BooleanConstructor;
        default: boolean;
    };
    hideGotoEndButtons: {
        type: BooleanConstructor;
        default: boolean;
    };
    labelFirstPage: {
        type: StringConstructor;
        default: string;
    };
    labelLastPage: {
        type: StringConstructor;
        default: string;
    };
    labelNextPage: {
        type: StringConstructor;
        default: string;
    };
    labelPage: {
        type: StringConstructor;
        default: string;
    };
    labelPrevPage: {
        type: StringConstructor;
        default: string;
    };
    lastClass: {
        type: (StringConstructor | ArrayConstructor)[];
        default: () => never[];
    };
    lastNumber: {
        type: BooleanConstructor;
        default: boolean;
    };
    lastText: {
        type: StringConstructor;
        default: string;
    };
    limit: {
        type: NumberConstructor;
        default: number;
    };
    modelValue: {
        type: NumberConstructor;
        default: number;
    };
    nextClass: {
        type: (StringConstructor | ArrayConstructor)[];
        default: () => never[];
    };
    nextText: {
        type: StringConstructor;
        default: string;
    };
    pageClass: {
        type: (StringConstructor | ArrayConstructor)[];
        default: () => never[];
    };
    perPage: {
        type: NumberConstructor;
        default: number;
    };
    pills: {
        type: BooleanConstructor;
        default: boolean;
    };
    prevClass: {
        type: (StringConstructor | ArrayConstructor)[];
        default: () => never[];
    };
    prevText: {
        type: StringConstructor;
        default: string;
    };
    size: {
        type: PropType<InputSize>;
        required: false;
    };
    totalRows: {
        type: NumberConstructor;
        default: number;
    };
}>> & {
    "onUpdate:modelValue"?: ((...args: any[]) => any) | undefined;
    "onPage-click"?: ((...args: any[]) => any) | undefined;
}, {
    modelValue: number;
    ariaLabel: string;
    disabled: boolean;
    align: Alignment;
    limit: number;
    pills: boolean;
    ellipsisClass: string | unknown[];
    ellipsisText: string;
    firstClass: string | unknown[];
    firstNumber: boolean;
    firstText: string;
    hideEllipsis: boolean;
    hideGotoEndButtons: boolean;
    labelFirstPage: string;
    labelLastPage: string;
    labelNextPage: string;
    labelPage: string;
    labelPrevPage: string;
    lastClass: string | unknown[];
    lastNumber: boolean;
    lastText: string;
    nextClass: string | unknown[];
    nextText: string;
    pageClass: string | unknown[];
    perPage: number;
    prevClass: string | unknown[];
    prevText: string;
    totalRows: number;
}>;
export default _sfc_main;
