import { Component, OnInit } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { ToastrService } from 'ngx-toastr';

import { AuthService } from '../auth/auth.service';
import { CommonService } from '@geonature_common/service/common.service';
import { ConfigService } from '@geonature/utils/configModule/core';

@Component({
  selector: 'pnx-login',
  templateUrl: 'login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  enable_sign_up: boolean = false;
  enable_user_management: boolean = false;
  public disableSubmit = false;

  identifiant: FormGroup;
  password: FormGroup;
  form: FormGroup;
  login_or_pass_recovery: boolean = false;

  constructor(
    private _authService: AuthService,
    private _toasterService: ToastrService,
    private _commonService: CommonService,
    private _configService: ConfigService
  ) {}

  ngOnInit() {
    if (this._configService.getSettings('CAS_PUBLIC.CAS_AUTHENTIFICATION')) {
      // if token not here here, redirection to CAS login page

      const url_redirection_cas = `${this._configService.getSettings(
        'CAS_PUBLIC.CAS_URL_LOGIN'
      )}?service=${this._configService.getSettings('API_ENDPOINT')}/gn_auth/login_cas`;
      document.location.href = url_redirection_cas;
    }
  }

  register(user) {
    this._authService.signinUser(user);
  }

  loginOrPwdRecovery(data) {
    this.disableSubmit = true;
    this._authService
      .loginOrPwdRecovery(data)
      .subscribe(
        res => {
          this._commonService.translateToaster('info', 'PasswordAndLoginRecovery');
        },
        error => {
          this._toasterService.error(error.error.msg, '');
        }
      )
      .add(() => {
        this.disableSubmit = false;
      });
  }
}
