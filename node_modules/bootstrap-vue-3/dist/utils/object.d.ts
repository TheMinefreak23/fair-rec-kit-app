export declare const assign: (target: any, ...args: any[]) => any;
export declare const defineProperties: (obj: any, props: PropertyDescriptorMap & ThisType<any>) => any;
export declare const defineProperty: (obj: any, prop: string | number | symbol, descriptor: PropertyDescriptor & ThisType<any>) => any;
export declare const omit: (obj: any, props: any) => any;
export declare const readonlyDescriptor: () => {
    enumerable: boolean;
    configurable: boolean;
    writable: boolean;
};
