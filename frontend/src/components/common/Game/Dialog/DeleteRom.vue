<script setup lang="ts">
import RAvatar from "@/components/common/Game/RAvatar.vue";
import RDialog from "@/components/common/RDialog.vue";
import romApi from "@/services/api/rom";
import storeRoms, { type SimpleRom } from "@/stores/roms";
import type { Events } from "@/types/emitter";
import { formatBytes } from "@/utils";
import type { Emitter } from "mitt";
import { inject, ref, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useDisplay, useTheme } from "vuetify";

// Props
const theme = useTheme();
const { smAndUp, mdAndUp } = useDisplay();
const router = useRouter();
const route = useRoute();
const show = ref(false);
const romsStore = storeRoms();
const roms = ref<SimpleRom[]>([]);
const romsToDeleteFromFs = ref<number[]>([]);
const platformId = ref<number>(0);
const emitter = inject<Emitter<Events>>("emitter");
emitter?.on("showDeleteRomDialog", (romsToDelete) => {
  roms.value = romsToDelete;
  platformId.value = roms.value[0].platform_id;
  updateDataTablePages();
  show.value = true;
});
const HEADERS = [
  {
    title: "Name",
    align: "start",
    sortable: true,
    key: "name",
  },
] as const;
const page = ref(1);
const itemsPerPage = ref(10);
const pageCount = ref(0);
const PER_PAGE_OPTIONS = [10, 25, 50, 100];

async function deleteRoms() {
  await romApi
    .deleteRoms({ roms: roms.value, deleteFromFs: romsToDeleteFromFs.value })
    .then((response) => {
      emitter?.emit("snackbarShow", {
        msg: response.data.msg,
        icon: "mdi-check-bold",
        color: "green",
      });
      romsStore.resetSelection();
      romsStore.remove(roms.value);
      emitter?.emit("refreshDrawer", null);
      closeDialog();
      if (route.name == "rom") {
        router.push({
          name: "platform",
          params: { platform: platformId.value },
        });
      }
    })
    .catch((error) => {
      console.log(error);
      emitter?.emit("snackbarShow", {
        msg: error.response.data.detail,
        icon: "mdi-close-circle",
        color: "red",
      });
      return;
    });
}

function updateDataTablePages() {
  pageCount.value = Math.ceil(roms.value.length / itemsPerPage.value);
}

watch(itemsPerPage, async () => {
  updateDataTablePages();
});

function closeDialog() {
  romsToDeleteFromFs.value = [];
  roms.value = [];
  show.value = false;
}
</script>

<template>
  <r-dialog
    @close="closeDialog"
    v-model="show"
    icon="mdi-delete"
    scroll-content
    :width="mdAndUp ? '50vw' : '95vw'"
  >
    <template #header>
      <v-row no-gutters class="justify-center">
        <span>Removing</span>
        <span class="text-romm-accent-1 mx-1">{{ roms.length }}</span>
        <span>games from RomM</span>
      </v-row>
    </template>
    <template #prepend>
      <v-list-item class="text-caption text-center">
        <span
          >Select the games you want to remove from your filesystem, otherwise
          they will only be deleted from RomM database.</span
        >
      </v-list-item>
    </template>
    <template #content>
      <v-data-table
        :item-value="(item) => item.id"
        :items="roms"
        :width="mdAndUp ? '60vw' : '95vw'"
        :items-per-page="itemsPerPage"
        :items-per-page-options="PER_PAGE_OPTIONS"
        :headers="HEADERS"
        v-model="romsToDeleteFromFs"
        v-model:page="page"
        show-select
      >
        <template #item.name="{ item }">
          <v-list-item class="px-0">
            <template #prepend>
              <r-avatar :rom="item" />
            </template>
            <v-row no-gutters
              ><v-col>{{ item.name }}</v-col></v-row
            >
            <v-row v-if="romsToDeleteFromFs.includes(item.id)" no-gutters
              ><v-col class="text-romm-accent-1"
                >{{ item.file_name
                }}<v-chip
                  v-if="romsToDeleteFromFs.includes(item.id) && smAndUp"
                  label
                  size="x-small"
                  class="text-romm-red ml-1"
                >
                  Removing from filesystem
                </v-chip></v-col
              ></v-row
            >
            <v-row
              v-if="romsToDeleteFromFs.includes(item.id) && !smAndUp"
              no-gutters
            >
              <v-col>
                <v-chip label size="x-small" class="text-romm-red">
                  Removing from filesystem
                </v-chip>
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col>
                <v-chip v-if="!smAndUp" size="x-small" label
                  >{{ formatBytes(item.file_size_bytes) }}
                </v-chip>
              </v-col>
            </v-row>
            <template #append>
              <v-row no-gutters v-if="smAndUp">
                <v-col>
                  <v-chip size="x-small" label>{{
                    formatBytes(item.file_size_bytes)
                  }}</v-chip>
                </v-col>
              </v-row>
            </template>
          </v-list-item>
        </template>
        <template #bottom>
          <v-divider />
          <v-row no-gutters class="pt-2 align-center justify-center">
            <v-col class="px-6">
              <v-pagination
                v-model="page"
                rounded="0"
                :show-first-last-page="true"
                active-color="romm-accent-1"
                :length="pageCount"
              />
            </v-col>
            <v-col cols="5" sm="3" xl="2">
              <v-select
                v-model="itemsPerPage"
                class="pa-2"
                label="Roms per page"
                density="compact"
                variant="outlined"
                :items="PER_PAGE_OPTIONS"
                hide-details
              />
            </v-col>
          </v-row>
        </template>
      </v-data-table>
    </template>
    <template #append>
      <v-row v-if="romsToDeleteFromFs.length > 0" no-gutters>
        <v-col>
          <v-list-item class="text-center mt-2">
            <span class="text-romm-red text-body-1">WARNING:</span>
            <span class="text-body-2 ml-1">You are going to remove</span>
            <span class="text-romm-red text-body-1 ml-1">{{
              romsToDeleteFromFs.length
            }}</span>
            <span class="text-body-2 ml-1"
              >roms from your filesystem. This action can't be reverted!</span
            >
          </v-list-item>
        </v-col>
      </v-row>
      <v-row class="justify-center my-2">
        <v-btn-group divided density="compact">
          <v-btn class="bg-terciary" @click="closeDialog" variant="flat">
            Cancel
          </v-btn>
          <v-btn
            class="text-romm-red bg-terciary"
            variant="flat"
            @click="deleteRoms"
          >
            Confirm
          </v-btn>
        </v-btn-group>
      </v-row>
    </template>
  </r-dialog>
</template>
