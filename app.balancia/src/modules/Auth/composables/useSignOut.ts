import { useToast } from 'primevue/usetoast';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import { useFirmBrand } from '@Composables';
import { HTTP_STATUS } from '@Enums';
import { getLoginPath } from '@Helpers';
import { resetAllStores } from '@Libraries';
import { useUserStore } from '@UserModule';
import { LogoutService } from '../services';

const TOAST_LIFE_MS = 5000;

/**
 * Signing out from a screen with no navbar — the not-found page (online QA 8.14, 24/11/2026: a
 * partner whose module was switched off saw "Esta página não existe", whose way back led to the
 * same page, and had no way to leave the session). It does what `TheNavbar`'s `onLogout` does,
 * which keeps its own copy (see Auth RULES, Known Gaps).
 *
 * Clearing the user is not clearing the app: the feature stores still hold the lists, drafts and
 * counters that belonged to whoever just left, and they guard their own fetches with "already
 * loaded" flags — so the next person to sign in inside this same SPA session saw the previous
 * one's data until a reload. `resetAllStores` skips `ui` (device preferences) and `colorScheme`
 * re-reads localStorage, so the theme and layout survive.
 *
 * A 401 on logout is the same destination: the server already has no session, so treating it as
 * a failure kept the person on a screen that looked signed in with a toast that lied.
 *
 * The host firm's kept brand goes too (Chrome QA 5.21): at the root it is the session's answer — a
 * view-as's firm — and the login that follows is the platform's.
 */
function useSignOut() {
  const userStore = useUserStore();

  const { forget: forgetFirmBrand } = useFirmBrand();
  const { push } = useRouter();
  const { t } = useI18n();
  const toast = useToast();

  // HELPERS
  function completeSignOut() {
    push(getLoginPath());

    userStore.clearUser();
    resetAllStores();
    forgetFirmBrand();

    toast.add({ severity: 'success', summary: t('auth.seeYouSoon'), life: TOAST_LIFE_MS });
  }

  // EVENTS
  function signOut() {
    return LogoutService()
      .then(completeSignOut)
      .catch((error: { response?: { status?: number } }) => {
        if (error?.response?.status === HTTP_STATUS.UNAUTHORIZED) {
          completeSignOut();
          return;
        }

        toast.add({ severity: 'error', summary: t('errors.somethingWentWrong'), life: TOAST_LIFE_MS });
      });
  }

  return { signOut };
}

export { useSignOut };
