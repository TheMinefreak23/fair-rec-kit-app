import { Ref } from 'vue';
declare function useEventListener(element: Ref<HTMLElement | undefined>, event: string, callback: EventListener): void;
export default useEventListener;
