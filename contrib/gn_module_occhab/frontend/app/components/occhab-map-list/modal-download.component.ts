import { Component, OnInit, Input } from "@angular/core";
import { NgbActiveModal } from "@ng-bootstrap/ng-bootstrap";
import { OccHabDataService } from "../../services/data.service";
import { OcchabStoreService } from "../../services/store.service";
@Component({
  selector: "pnx-occhab-map-list-download-modal",
  templateUrl: "modal-download.component.html"
})
export class OccHabModalDownloadComponent implements OnInit {
  @Input() tooManyObs = false;
  constructor(
    public activeModal: NgbActiveModal,
    private _occHabDataService: OccHabDataService,
    public storeService: OcchabStoreService
  ) {}

  ngOnInit() {}

  downloadStations(exportFormat: string) {
    this._occHabDataService.exportStations(
      exportFormat,
      this.storeService.idsStation
    );
  }
}
