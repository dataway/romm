import type {
  CollectionSchema,
  VirtualCollectionSchema,
} from "@/__generated__";
import { uniqBy } from "lodash";
import { defineStore } from "pinia";
import type { SimpleRom } from "./roms";

export type Collection = CollectionSchema;
export type VirtualCollection = VirtualCollectionSchema;

export default defineStore("collections", {
  state: () => ({
    allCollections: [] as Collection[],
    virtualCollections: [] as VirtualCollection[],
    favCollection: {} as Collection | undefined,
    searchText: "" as string,
  }),
  getters: {
    filteredCollections: ({ allCollections, searchText }) =>
      allCollections.filter((p) =>
        p.name.toLowerCase().includes(searchText.toLowerCase()),
      ),
    filteredVirtualCollections: ({ virtualCollections, searchText }) =>
      virtualCollections.filter((p) =>
        p.name.toLowerCase().includes(searchText.toLowerCase()),
      ),
  },
  actions: {
    _reorder() {
      this.allCollections = this.allCollections.sort((a, b) => {
        return a.name.localeCompare(b.name);
      });
      this.allCollections = uniqBy(this.allCollections, "id");
    },
    setFavCollection(favCollection: Collection | undefined) {
      this.favCollection = favCollection;
    },
    set(collections: Collection[]) {
      this.allCollections = collections;
    },
    setVirtual(collections: VirtualCollection[]) {
      this.virtualCollections = collections;
    },
    add(collection: Collection) {
      this.allCollections.push(collection);
      this._reorder();
    },
    update(collection: Collection) {
      this.allCollections = this.allCollections.map((value) =>
        value.id === collection.id ? collection : value,
      );
      this._reorder();
    },
    exists(collection: Collection) {
      return (
        this.allCollections.filter((p) => p.name == collection.name).length > 0
      );
    },
    remove(collection: Collection) {
      this.allCollections = this.allCollections.filter((p) => {
        return p.name !== collection.name;
      });
    },
    get(collectionId: number) {
      return this.allCollections.find((p) => p.id === collectionId);
    },
    isFav(rom: SimpleRom) {
      return this.favCollection?.rom_ids?.includes(rom.id);
    },
    isVirtualCollection(
      collection: Collection | VirtualCollection,
    ): collection is VirtualCollection {
      return (
        collection &&
        typeof collection === "object" &&
        "id" in collection &&
        "name" in collection &&
        "virtual" in collection
      );
    },
    reset() {
      this.allCollections = [];
      this.virtualCollections = [];
      this.favCollection = undefined;
      this.searchText = "";
    },
  },
});
