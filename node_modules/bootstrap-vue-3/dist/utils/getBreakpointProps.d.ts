declare type PropDefinition = {
    type: any[];
    default: any;
};
interface ComponentProps {
    [key: string]: PropDefinition;
}
declare const _default: (prefix: string, breakpoints: string[], definition: PropDefinition) => ComponentProps;
export default _default;
