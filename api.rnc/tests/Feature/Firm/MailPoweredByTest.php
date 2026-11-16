<?php

use App\Mail\EmailVerificationCodeMail;
use App\Modules\Firm\Models\Firm;
use App\Modules\Firm\Services\CurrentFirm;
use App\Modules\Firm\Services\MailBrand;
use Illuminate\Support\Facades\Mail;

/*
 * The product signs a tenant's e-mail, discreetly (brand/SYSTEM.md §5): the icon at 16px and
 * "powered by Balancia" in the footer's grey. The platform's own messages are already Balancia's
 * and carry no signature.
 */
beforeEach(function () {
    config(['platform.name' => 'Balancia']);
});

describe('the powered-by signature', function () {
    it('signs a tenant firm\'s e-mail with the product\'s name and its 16px icon', function () {
        $firm = Firm::factory()->create(['slug' => 'alvorada', 'is_platform' => false]);

        $html = view('mail.layout', ['mailBrand' => MailBrand::fromFirm($firm)])->render();

        expect(MailBrand::fromFirm($firm)->poweredBy)->toBe('Balancia')
            ->and($html)->toContain('powered by Balancia')
            ->and($html)->toContain('width="16" height="16"')
            ->and($html)->toContain('data:image/png;base64,');
    });

    it('leaves the platform firm\'s e-mail unsigned', function () {
        $platform = Firm::factory()->create(['slug' => 'balancia', 'is_platform' => true]);

        expect(MailBrand::fromFirm($platform)->poweredBy)->toBeNull()
            ->and(view('mail.layout', ['mailBrand' => MailBrand::fromFirm($platform)])->render())->not->toContain('powered by');
    });

    it('leaves the platform\'s own e-mail unsigned, in Balancia\'s teal', function () {
        $brand = MailBrand::platform();

        expect($brand->poweredBy)->toBeNull()
            ->and($brand->ink)->toBe('#0e5a5c')
            ->and($brand->accent)->toBe('#2fb7a3');
    });

    it('signs the plain-text alternative too', function () {
        $firm = Firm::factory()->create(['slug' => 'alvorada', 'is_platform' => false]);

        $text = view('mail.verification-code-text', ['mailBrand' => MailBrand::fromFirm($firm), 'code' => '123456', 'ttlMinutes' => 10])->render();

        expect($text)->toContain('powered by Balancia');
    });

    it('embeds the icon as an inline part when a real message is sent', function () {
        config(['mail.default' => 'array']);
        app(CurrentFirm::class)->set(Firm::factory()->create(['slug' => 'alvorada', 'is_platform' => false]));

        expect(resource_path('images/mail/powered-by-icon.png'))->toBeFile();

        Mail::to('cliente@exemplo.test')->send(new EmailVerificationCodeMail('123456'));

        $email = app('mailer')->getSymfonyTransport()->messages()->first()->getOriginalMessage();
        $inline = collect($email->getAttachments())->filter(fn ($part) => $part->getDisposition() === 'inline');

        expect($inline)->toHaveCount(1)
            ->and($inline->first()->getContentType())->toBe('image/png')
            ->and($email->getHtmlBody())->toContain('cid:')
            ->and($email->getHtmlBody())->toContain('powered by Balancia')
            ->and($email->getHtmlBody())->not->toContain('data:image/png;base64,');
    });
});
